# -*- coding: utf-8 -*-
import base64
import io
from datetime import datetime, time

import xlsxwriter

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductionVarianceWizard(models.TransientModel):
    _name = 'coa.production.variance.wizard'
    _description = 'Production Variance Report Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    product_ids = fields.Many2many('product.product', string='Products',
                                   domain=[('type', '!=', 'service')])
    categ_ids = fields.Many2many('product.category', string='Product Categories')
    partner_ids = fields.Many2many('res.partner', string='Customers',
                                   domain=[('customer_rank', '>', 0)])
    mto_only = fields.Boolean(string='MTO Only (Linked to Sale Order)', default=False)
    state_filter = fields.Selection([
        ('all', 'All (except Cancelled)'),
        ('done', 'Done Only'),
        ('progress', 'In Progress / To Close'),
    ], string='MO State', default='done', required=True)
    variance_filter = fields.Selection([
        ('all', 'All Orders'),
        ('with_variance', 'With Variance Only'),
        ('under', 'Under-Produced Only'),
        ('over', 'Over-Produced Only'),
    ], string='Variance', default='all', required=True)

    xlsx_file = fields.Binary(string='Excel File', readonly=True)
    xlsx_filename = fields.Char(string='Excel Filename', readonly=True)

    # ------------------------------------------------------------------
    # Domain / Data
    # ------------------------------------------------------------------
    def _get_domain(self):
        self.ensure_one()
        domain = [('company_id', 'in', self.env.companies.ids)]
        if self.date_from:
            domain.append(('date_finished', '>=',
                           datetime.combine(self.date_from, time.min)))
        if self.date_to:
            domain.append(('date_finished', '<=',
                           datetime.combine(self.date_to, time.max)))
        if self.product_ids:
            domain.append(('product_id', 'in', self.product_ids.ids))
        if self.categ_ids:
            domain.append(('categ_id', 'child_of', self.categ_ids.ids))
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))
        if self.mto_only:
            domain.append(('sale_id', '!=', False))
        if self.state_filter == 'done':
            domain.append(('state', '=', 'done'))
        elif self.state_filter == 'progress':
            domain.append(('state', 'in', ('progress', 'to_close')))
        if self.variance_filter == 'with_variance':
            domain.append(('variance_qty', '!=', 0))
        elif self.variance_filter == 'under':
            domain.append(('variance_qty', '<', 0))
        elif self.variance_filter == 'over':
            domain.append(('variance_qty', '>', 0))
        return domain

    def _get_lines(self):
        self.ensure_one()
        return self.env['coa.mfg.production.variance'].search(
            self._get_domain(), order='date_finished desc, id desc')

    @api.model
    def _get_totals(self, lines):
        total_planned = sum(lines.mapped('planned_qty'))
        total_produced = sum(lines.mapped('produced_qty'))
        total_variance = total_produced - total_planned
        total_percent = (total_variance / total_planned * 100.0) if total_planned else 0.0
        return {
            'ordered': sum(lines.mapped('ordered_qty')),
            'delivered': sum(lines.mapped('delivered_qty')),
            'planned': total_planned,
            'produced': total_produced,
            'variance': total_variance,
            'percent': total_percent,
        }

    # ------------------------------------------------------------------
    # PDF
    # ------------------------------------------------------------------
    def action_print_pdf(self):
        self.ensure_one()
        if not self._get_lines():
            raise UserError(_('No data found for the selected filters.'))
        return self.env.ref(
            'coa_mfg_production_variance.action_report_production_variance_pdf'
        ).report_action(self)

    # ------------------------------------------------------------------
    # Excel
    # ------------------------------------------------------------------
    def action_export_xlsx(self):
        self.ensure_one()
        lines = self._get_lines()
        if not lines:
            raise UserError(_('No data found for the selected filters.'))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Production Variance')

        # ---- Formats
        fmt_title = workbook.add_format({
            'bold': True, 'font_size': 16, 'align': 'center',
            'valign': 'vcenter', 'font_color': '#1F4E78'})
        fmt_subtitle = workbook.add_format({
            'italic': True, 'font_size': 9, 'align': 'center',
            'font_color': '#666666'})
        fmt_header = workbook.add_format({
            'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white',
            'align': 'center', 'valign': 'vcenter', 'border': 1,
            'text_wrap': True})
        fmt_text = workbook.add_format({'border': 1, 'valign': 'vcenter'})
        fmt_date = workbook.add_format({
            'border': 1, 'align': 'center', 'num_format': 'yyyy-mm-dd hh:mm'})
        fmt_num = workbook.add_format({
            'border': 1, 'num_format': '#,##0.00', 'align': 'right'})
        fmt_num_red = workbook.add_format({
            'border': 1, 'num_format': '#,##0.00', 'align': 'right',
            'font_color': '#C00000', 'bold': True})
        fmt_num_green = workbook.add_format({
            'border': 1, 'num_format': '#,##0.00', 'align': 'right',
            'font_color': '#2E7D32', 'bold': True})
        fmt_pct = workbook.add_format({
            'border': 1, 'num_format': '#,##0.00"%"', 'align': 'right'})
        fmt_pct_red = workbook.add_format({
            'border': 1, 'num_format': '#,##0.00"%"', 'align': 'right',
            'font_color': '#C00000', 'bold': True})
        fmt_pct_green = workbook.add_format({
            'border': 1, 'num_format': '#,##0.00"%"', 'align': 'right',
            'font_color': '#2E7D32', 'bold': True})
        fmt_total_label = workbook.add_format({
            'bold': True, 'bg_color': '#D9E2F3', 'border': 1,
            'align': 'right'})
        fmt_total_num = workbook.add_format({
            'bold': True, 'bg_color': '#D9E2F3', 'border': 1,
            'num_format': '#,##0.00', 'align': 'right'})
        fmt_total_pct = workbook.add_format({
            'bold': True, 'bg_color': '#D9E2F3', 'border': 1,
            'num_format': '#,##0.00"%"', 'align': 'right'})

        headers = [
            _('Manufacturing Order'), _('Sale Order'), _('Customer'),
            _('Product'), _('Category'),
            _('Responsible'), _('End Date'), _('State'), _('UoM'),
            _('Ordered Qty (SO)'), _('Planned Qty'), _('Produced Qty'),
            _('Delivered Qty'), _('Variance Qty'), _('Variance %'),
        ]
        widths = [18, 14, 28, 35, 22, 20, 18, 12, 10, 14, 14, 14, 14, 14, 12]
        for col, width in enumerate(widths):
            sheet.set_column(col, col, width)

        # ---- Title + filters info
        last_col = len(headers) - 1
        sheet.merge_range(0, 0, 0, last_col,
                          _('Production Variance Report (Planned vs Produced)'),
                          fmt_title)
        sheet.set_row(0, 28)
        filters_txt = []
        if self.date_from:
            filters_txt.append(_('From: %s') % self.date_from)
        if self.date_to:
            filters_txt.append(_('To: %s') % self.date_to)
        filters_txt.append(dict(self._fields['state_filter'].selection).get(self.state_filter))
        filters_txt.append(dict(self._fields['variance_filter'].selection).get(self.variance_filter))
        sheet.merge_range(1, 0, 1, last_col, ' | '.join(filters_txt), fmt_subtitle)

        # ---- Header row
        header_row = 3
        for col, header in enumerate(headers):
            sheet.write(header_row, col, header, fmt_header)
        sheet.freeze_panes(header_row + 1, 0)
        sheet.autofilter(header_row, 0, header_row, last_col)

        # ---- Data rows
        state_labels = dict(
            self.env['coa.mfg.production.variance']._fields['state'].selection)
        row = header_row + 1
        for line in lines:
            variance = line.variance_qty
            f_num = fmt_num_red if variance < 0 else (
                fmt_num_green if variance > 0 else fmt_num)
            f_pct = fmt_pct_red if variance < 0 else (
                fmt_pct_green if variance > 0 else fmt_pct)
            sheet.write(row, 0, line.production_id.name or '', fmt_text)
            sheet.write(row, 1, line.sale_id.name or '', fmt_text)
            sheet.write(row, 2, line.partner_id.display_name or '', fmt_text)
            sheet.write(row, 3, line.product_id.display_name or '', fmt_text)
            sheet.write(row, 4, line.categ_id.display_name or '', fmt_text)
            sheet.write(row, 5, line.user_id.name or '', fmt_text)
            sheet.write(row, 6,
                        fields.Datetime.context_timestamp(
                            self, line.date_finished
                        ).replace(tzinfo=None) if line.date_finished else '',
                        fmt_date)
            sheet.write(row, 7, state_labels.get(line.state, ''), fmt_text)
            sheet.write(row, 8, line.product_uom_id.name or '', fmt_text)
            sheet.write_number(row, 9, line.ordered_qty, fmt_num)
            sheet.write_number(row, 10, line.planned_qty, fmt_num)
            sheet.write_number(row, 11, line.produced_qty, fmt_num)
            sheet.write_number(row, 12, line.delivered_qty, fmt_num)
            sheet.write_number(row, 13, variance, f_num)
            sheet.write_number(row, 14, line.variance_percent, f_pct)
            row += 1

        # ---- Totals (percentage = sum variance / sum planned, not avg)
        totals = self._get_totals(lines)
        sheet.merge_range(row, 0, row, 8, _('TOTALS'), fmt_total_label)
        sheet.write_number(row, 9, totals['ordered'], fmt_total_num)
        sheet.write_number(row, 10, totals['planned'], fmt_total_num)
        sheet.write_number(row, 11, totals['produced'], fmt_total_num)
        sheet.write_number(row, 12, totals['delivered'], fmt_total_num)
        sheet.write_number(row, 13, totals['variance'], fmt_total_num)
        sheet.write_number(row, 14, totals['percent'], fmt_total_pct)

        workbook.close()
        output.seek(0)

        self.write({
            'xlsx_file': base64.b64encode(output.getvalue()),
            'xlsx_filename': 'Production_Variance_%s.xlsx' % fields.Date.to_string(
                fields.Date.context_today(self)),
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s/%s/xlsx_file/%s?download=true' % (
                self._name, self.id, self.xlsx_filename),
            'target': 'self',
        }

    # ------------------------------------------------------------------
    # Open interactive view (bonus)
    # ------------------------------------------------------------------
    def action_open_view(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'coa_mfg_production_variance.action_coa_production_variance')
        action['domain'] = self._get_domain()
        action['context'] = {}
        return action
