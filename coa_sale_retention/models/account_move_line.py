# -*- coding: utf-8 -*-
import base64
import io
from datetime import datetime

from odoo import _, models
from odoo.exceptions import UserError

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def action_export_retention_xlsx(self):
        """Export the selected journal items as an Excel workbook grouped
        by partner (used by the 'Retention Receivables (Excel)' action)."""
        if not self:
            raise UserError(_("Select the lines to export first."))
        if xlsxwriter is None:
            raise UserError(_("The Python library 'xlsxwriter' is not "
                              "installed on the server."))

        lines = self.sorted(
            key=lambda l: (l.partner_id.display_name or "", l.date or "")
        )
        buf = io.BytesIO()
        workbook = xlsxwriter.Workbook(buf, {"in_memory": True})
        sheet = workbook.add_worksheet(_("Retention Receivables"))

        title_fmt = workbook.add_format({"bold": True, "font_size": 14})
        header_fmt = workbook.add_format({
            "bold": True, "bg_color": "#875A7B", "font_color": "#FFFFFF",
            "border": 1,
        })
        partner_fmt = workbook.add_format({
            "bold": True, "bg_color": "#EEEEEE",
        })
        partner_money_fmt = workbook.add_format({
            "bold": True, "bg_color": "#EEEEEE", "num_format": "#,##0.00",
        })
        date_fmt = workbook.add_format({"num_format": "yyyy-mm-dd"})
        money_fmt = workbook.add_format({"num_format": "#,##0.00"})
        total_fmt = workbook.add_format({
            "bold": True, "num_format": "#,##0.00", "top": 6,
        })
        total_label_fmt = workbook.add_format({"bold": True, "top": 6})

        headers = [_("Date"), _("Journal Entry"), _("Label"),
                   _("Due Date"), _("Debit"), _("Credit"), _("Residual")]
        widths = [12, 20, 45, 12, 15, 15, 15]
        for col, width in enumerate(widths):
            sheet.set_column(col, col, width)

        sheet.write(0, 0, _("Retention Receivables"), title_fmt)
        sheet.write(1, 0, _("Printed on: %s",
                            datetime.now().strftime("%Y-%m-%d %H:%M")))

        row = 3
        for col, header in enumerate(headers):
            sheet.write(row, col, header, header_fmt)
        row += 1

        def write_money_row(r, fmt, debit, credit, residual):
            sheet.write_number(r, 4, debit, fmt)
            sheet.write_number(r, 5, credit, fmt)
            sheet.write_number(r, 6, residual, fmt)

        grand = {"debit": 0.0, "credit": 0.0, "residual": 0.0}
        for partner in lines.mapped("partner_id").sorted("display_name"):
            partner_lines = lines.filtered(
                lambda l, p=partner: l.partner_id == p
            )
            sheet.merge_range(row, 0, row, 3,
                              partner.display_name, partner_fmt)
            sub = {"debit": 0.0, "credit": 0.0, "residual": 0.0}
            sub_row = row
            row += 1
            for line in partner_lines:
                if line.date:
                    sheet.write_datetime(row, 0, line.date, date_fmt)
                sheet.write(row, 1, line.move_id.name or "")
                sheet.write(row, 2, line.name or "")
                if line.date_maturity:
                    sheet.write_datetime(row, 3, line.date_maturity, date_fmt)
                write_money_row(row, money_fmt, line.debit, line.credit,
                                line.amount_residual)
                sub["debit"] += line.debit
                sub["credit"] += line.credit
                sub["residual"] += line.amount_residual
                row += 1
            write_money_row(sub_row, partner_money_fmt,
                            sub["debit"], sub["credit"], sub["residual"])
            for key in grand:
                grand[key] += sub[key]

        for col in range(4):
            sheet.write(row, col, _("Total") if col == 0 else "",
                        total_label_fmt)
        write_money_row(row, total_fmt,
                        grand["debit"], grand["credit"], grand["residual"])

        workbook.close()
        attachment = self.env["ir.attachment"].create({
            "name": "retention_receivables.xlsx",
            "datas": base64.b64encode(buf.getvalue()),
            "mimetype": "application/vnd.openxmlformats-officedocument"
                        ".spreadsheetml.sheet",
        })
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=true" % attachment.id,
            "target": "self",
        }
