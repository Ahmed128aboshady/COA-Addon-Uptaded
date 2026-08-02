# -*- coding: utf-8 -*-
import io
import base64
import xlsxwriter
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import defaultdict


class CommissionAnalysisWizard(models.TransientModel):
    _name = 'commission.analysis.wizard'
    _description = 'تقرير تحليل مبيعات المندوبين'

    date_from = fields.Date(string='من تاريخ', required=True)
    date_to = fields.Date(string='إلى تاريخ', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        today = date.today()
        first_day = today.replace(day=1)
        last_day = (first_day + relativedelta(months=1)) - relativedelta(days=1)
        res.setdefault('date_from', first_day)
        res.setdefault('date_to', last_day)
        return res
    salesperson_ids = fields.Many2many(
        'res.users',
        string='المندوبون',
        domain=[('share', '=', False)],
        help='اتركه فارغاً لعرض جميع المندوبين تلقائياً.',
    )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise UserError(_('تاريخ البداية يجب أن يكون قبل تاريخ النهاية.'))

    def action_print_report(self):
        self.ensure_one()
        return self.env.ref(
            'commission_sales.action_commission_analysis_report'
        ).report_action(self)

    def action_export_excel(self):
        """تصدير التقرير كملف Excel (XLSX)."""
        self.ensure_one()
        data = self.get_report_data()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('تقرير العمولات')

        # ───── Formats ─────
        title_fmt = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center',
            'fg_color': '#1F4E79', 'font_color': 'white', 'border': 1,
        })
        header_fmt = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter',
            'fg_color': '#2E75B6', 'font_color': 'white',
            'border': 1, 'text_wrap': True,
        })
        money_fmt = workbook.add_format({
            'num_format': '#,##0.00', 'border': 1, 'align': 'right',
        })
        money_red_fmt = workbook.add_format({
            'num_format': '#,##0.00', 'border': 1, 'align': 'right',
            'font_color': '#C00000',
        })
        money_green_fmt = workbook.add_format({
            'num_format': '#,##0.00', 'border': 1, 'align': 'right',
            'font_color': '#375623', 'bold': True,
        })
        text_fmt = workbook.add_format({'border': 1})
        total_fmt = workbook.add_format({
            'bold': True, 'border': 1, 'fg_color': '#D9E1F2',
            'num_format': '#,##0.00', 'align': 'right',
        })
        total_lbl_fmt = workbook.add_format({
            'bold': True, 'border': 1, 'fg_color': '#D9E1F2',
        })

        # ───── Title ─────
        currency_symbol = data['currency'].symbol or data['currency'].name
        sheet.merge_range(0, 0, 0, 4,
            'تقرير تحليل مبيعات المندوبين', title_fmt)
        sheet.merge_range(1, 0, 1, 4,
            f"الفترة من {data['date_from']} إلى {data['date_to']}  |  العملة: {currency_symbol}",
            workbook.add_format({'align': 'center', 'italic': True}))

        # ───── Headers ─────
        headers = ['المندوب', 'المبيعات', 'المرتجعات', 'صافي المبيعات', 'العمولة المستحقة']
        col_widths = [30, 18, 18, 18, 20]
        for col, (h, w) in enumerate(zip(headers, col_widths)):
            sheet.write(3, col, h, header_fmt)
            sheet.set_column(col, col, w)

        # ───── Data rows ─────
        row = 4
        for r in data['rows']:
            sheet.write(row, 0, r['salesperson'], text_fmt)
            sheet.write(row, 1, r['invoiced'], money_fmt)
            sheet.write(row, 2, r['refunded'], money_red_fmt)
            sheet.write(row, 3, r['net'], money_fmt)
            sheet.write(row, 4, r['commission'], money_green_fmt)
            row += 1

        # ───── Totals row ─────
        t = data['totals']
        sheet.write(row, 0, 'الإجمالي', total_lbl_fmt)
        sheet.write(row, 1, t['invoiced'], total_fmt)
        sheet.write(row, 2, t['refunded'], total_fmt)
        sheet.write(row, 3, t['net'], total_fmt)
        sheet.write(row, 4, t['commission'], total_fmt)

        workbook.close()
        xlsx_data = output.getvalue()

        # حفظ كـ attachment وإرجاع رابط تنزيل
        filename = f"تقرير_العمولات_{data['date_from']}_{data['date_to']}.xlsx"
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(xlsx_data),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def get_report_data(self):
        """
        يجلب البيانات من Invoice Analysis (account.invoice.report)
        ويرجع قائمة بصافي مبيعات كل مندوب وعمولته.
        """
        self.ensure_one()

        domain = [
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
        ]
        if self.salesperson_ids:
            domain.append(('invoice_user_id', 'in', self.salesperson_ids.ids))

        # جلب سجلات Invoice Analysis
        inv_lines = self.env['account.invoice.report'].search(domain)

        if not inv_lines:
            raise UserError(_(
                'لا توجد فواتير مؤكدة في هذه الفترة.'
            ))

        # تجميع البيانات حسب المندوب
        sp_data = defaultdict(lambda: {'invoiced': 0.0, 'refunded': 0.0})

        for line in inv_lines:
            sp = line.invoice_user_id
            # price_subtotal: موجب للفواتير، سالب للمرتجعات في invoice analysis
            amount = abs(line.price_subtotal)
            if line.move_type == 'out_invoice':
                sp_data[sp]['invoiced'] += amount
            elif line.move_type == 'out_refund':
                sp_data[sp]['refunded'] += amount

        # جلب نسب العمولة النشطة لحساب العمولة
        rates = self.env['commission.rate'].search([('active', '=', True)])

        rows = []
        total_invoiced = 0.0
        total_refunded = 0.0
        total_net = 0.0
        total_commission = 0.0

        for sp, data in sorted(sp_data.items(), key=lambda x: x[0].name):
            invoiced = data['invoiced']
            refunded = data['refunded']
            net = invoiced - refunded

            # حساب العمولة: نجلب الفواتير التفصيلية للمندوب حسب تاج العميل
            commission = self._compute_salesperson_commission(sp, rates)

            total_invoiced += invoiced
            total_refunded += refunded
            total_net += net
            total_commission += commission

            rows.append({
                'salesperson': sp.name,
                'invoiced': invoiced,
                'refunded': refunded,
                'net': net,
                'commission': commission,
            })

        return {
            'rows': rows,
            'totals': {
                'invoiced': total_invoiced,
                'refunded': total_refunded,
                'net': total_net,
                'commission': total_commission,
            },
            'currency': self.env.company.currency_id,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }

    def _compute_salesperson_commission(self, salesperson, rates):
        """
        يحسب عمولة مندوب واحد بناءً على تاجات عملائه
        من Invoice Analysis للفترة المحددة.
        """
        if not rates:
            return 0.0

        tag_rate_map = {r.customer_tag_id.id: r for r in rates}
        tag_ids = list(tag_rate_map.keys())

        # جلب الفواتير من account.invoice.report للمندوب
        inv_lines = self.env['account.invoice.report'].search([
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('invoice_user_id', '=', salesperson.id),
        ])

        # تجميع صافي المبيعات حسب تاج العميل
        tag_net = defaultdict(float)
        for line in inv_lines:
            partner_tags = set(line.partner_id.category_id.ids) & set(tag_ids)
            amount = abs(line.price_subtotal)
            sign = 1 if line.move_type == 'out_invoice' else -1
            for tag_id in partner_tags:
                tag_net[tag_id] += amount * sign

        # حساب العمولة لكل تاج
        total_commission = 0.0
        for tag_id, net in tag_net.items():
            rate_rec = tag_rate_map.get(tag_id)
            if rate_rec:
                total_commission += rate_rec.compute_commission(net)

        return total_commission
