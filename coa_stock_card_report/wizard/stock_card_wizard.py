import io
import base64
from datetime import datetime, time

from odoo import models, fields, api, _
from odoo.exceptions import UserError

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class StockCardReportWizard(models.TransientModel):
    _name = 'stock.card.report.wizard'
    _description = 'Stock Card Report Wizard'

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = _('Stock Card Report')

    product_ids = fields.Many2many(
        'product.product',
        string='Products',
        domain="[('is_storable', '=', True)]",
    )
    location_ids = fields.Many2many(
        'stock.location',
        string='Locations',
        domain="[('usage', '=', 'internal')]",
    )
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    line_ids = fields.One2many(
        'stock.card.report.line', 'wizard_id', string='Report Lines', readonly=True,
    )
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company,
    )

    def _validate_dates(self):
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise UserError(_('Date From (%s) cannot be after Date To (%s).', self.date_from, self.date_to))

    def _get_products(self):
        if self.product_ids:
            return self.product_ids
        return self.env['product.product'].search([
            ('is_storable', '=', True),
            ('company_id', 'in', [self.company_id.id, False]),
        ])

    def _get_locations(self):
        if self.location_ids:
            return self.location_ids
        return self.env['stock.location'].search([
            ('usage', '=', 'internal'),
            ('company_id', 'in', [self.company_id.id, False]),
        ])

    def _get_stock_card_data(self):
        """Compute stock card lines for each (product, location) pair."""
        products = self._get_products()
        locations = self._get_locations()

        date_from_dt = (
            datetime.combine(self.date_from, time.min) if self.date_from else None
        )
        date_to_dt = (
            datetime.combine(self.date_to, time.max) if self.date_to else None
        )

        lines = []
        MoveLine = self.env['stock.move.line'].sudo()

        for product in products:
            for location in locations:
                section_lines = []
                running_balance = 0.0

                # --- Opening Balance ---
                if date_from_dt:
                    domain_before = [
                        ('state', '=', 'done'),
                        ('product_id', '=', product.id),
                        ('date', '<', date_from_dt),
                    ]
                    qty_in = sum(
                        MoveLine.search(
                            domain_before + [('location_dest_id', '=', location.id)]
                        ).mapped('quantity_product_uom')
                    )
                    qty_out = sum(
                        MoveLine.search(
                            domain_before + [('location_id', '=', location.id)]
                        ).mapped('quantity_product_uom')
                    )
                    running_balance = qty_in - qty_out
                    if running_balance or qty_in or qty_out:
                        section_lines.append({
                            'product_id': product.id,
                            'location_id': location.id,
                            'date': date_from_dt,
                            'reference': _('Opening Balance'),
                            'location_from': '',
                            'location_to': '',
                            'qty_in': 0.0,
                            'qty_out': 0.0,
                            'balance': running_balance,
                            'product_uom': product.uom_id.name,
                            'is_opening': True,
                        })

                # --- Moves in range ---
                domain_moves = [
                    ('state', '=', 'done'),
                    ('product_id', '=', product.id),
                    '|',
                    ('location_id', '=', location.id),
                    ('location_dest_id', '=', location.id),
                ]
                if date_from_dt:
                    domain_moves.append(('date', '>=', date_from_dt))
                if date_to_dt:
                    domain_moves.append(('date', '<=', date_to_dt))

                move_lines = MoveLine.search(domain_moves, order='date asc, id asc')

                for ml in move_lines:
                    # Skip internal transfers within the same location
                    if ml.location_id.id == ml.location_dest_id.id:
                        continue

                    qty_in = 0.0
                    qty_out = 0.0
                    if ml.location_dest_id.id == location.id:
                        qty_in = ml.quantity_product_uom
                    if ml.location_id.id == location.id:
                        qty_out = ml.quantity_product_uom

                    running_balance += qty_in - qty_out

                    section_lines.append({
                        'product_id': product.id,
                        'location_id': location.id,
                        'date': ml.date,
                        'reference': ml.reference or '',
                        'location_from': ml.location_id.complete_name or '',
                        'location_to': ml.location_dest_id.complete_name or '',
                        'qty_in': qty_in,
                        'qty_out': qty_out,
                        'balance': running_balance,
                        'product_uom': product.uom_id.name,
                        'is_opening': False,
                    })

                # Only include sections that have data
                if section_lines:
                    lines.extend(section_lines)

        return lines

    def action_view_report(self):
        self.ensure_one()
        self._validate_dates()
        self.line_ids.unlink()

        data = self._get_stock_card_data()
        if not data:
            raise UserError(_('No stock moves found for the selected criteria.'))

        line_vals = []
        for d in data:
            line_vals.append(dict(d, wizard_id=self.id))
        self.env['stock.card.report.line'].create(line_vals)

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_export_excel(self):
        self.ensure_one()
        self._validate_dates()
        if not xlsxwriter:
            raise UserError(_('The xlsxwriter library is required to export Excel files.'))

        data = self._get_stock_card_data()
        if not data:
            raise UserError(_('No stock moves found for the selected criteria.'))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Stock Card')

        # --- Styles ---
        fmt_company = workbook.add_format({
            'bold': True, 'font_size': 16, 'align': 'center',
            'font_color': '#2F5496',
        })
        fmt_title = workbook.add_format({
            'bold': True, 'font_size': 11, 'align': 'center',
        })
        fmt_date_range = workbook.add_format({
            'bold': True, 'font_size': 11, 'align': 'center',
        })
        fmt_section = workbook.add_format({
            'bold': True, 'font_size': 11, 'bg_color': '#D6E4F0',
            'border': 1,
        })
        fmt_header = workbook.add_format({
            'bold': True, 'font_size': 10, 'bg_color': '#2F5496',
            'font_color': 'white', 'border': 1, 'align': 'center',
        })
        fmt_text = workbook.add_format({
            'font_size': 10, 'border': 1,
        })
        fmt_number = workbook.add_format({
            'font_size': 10, 'border': 1, 'num_format': '#,##0.00',
        })
        fmt_date_cell = workbook.add_format({
            'font_size': 10, 'border': 1, 'num_format': 'yyyy-mm-dd hh:mm',
        })
        fmt_opening_text = workbook.add_format({
            'font_size': 10, 'border': 1, 'bold': True, 'italic': True,
            'bg_color': '#FFF2CC',
        })
        fmt_opening_number = workbook.add_format({
            'font_size': 10, 'border': 1, 'bold': True, 'italic': True,
            'bg_color': '#FFF2CC', 'num_format': '#,##0.00',
        })
        fmt_opening_date = workbook.add_format({
            'font_size': 10, 'border': 1, 'bold': True, 'italic': True,
            'bg_color': '#FFF2CC', 'num_format': 'yyyy-mm-dd hh:mm',
        })

        # Column widths
        col_widths = [20, 22, 30, 30, 14, 14, 16]
        for i, w in enumerate(col_widths):
            sheet.set_column(i, i, w)

        row = 0

        # Company name
        sheet.merge_range(row, 0, row, 6, self.company_id.name or '', fmt_company)
        row += 1

        # Report title
        sheet.merge_range(row, 0, row, 6, 'Stock Card Report', fmt_title)
        row += 1

        # Date range
        date_info_parts = []
        if self.date_from:
            date_info_parts.append('From: %s' % self.date_from)
        if self.date_to:
            date_info_parts.append('To: %s' % self.date_to)
        date_info = '  |  '.join(date_info_parts) if date_info_parts else 'All dates'
        sheet.merge_range(row, 0, row, 6, date_info, fmt_date_range)
        row += 2

        # Group lines by (product, location)
        current_key = None
        for line in data:
            key = (line['product_id'], line['location_id'])
            if key != current_key:
                current_key = key
                product = self.env['product.product'].browse(line['product_id'])
                location = self.env['stock.location'].browse(line['location_id'])
                # Section header
                section_title = '%s  -  %s  [%s]' % (
                    product.display_name, location.complete_name, line['product_uom'],
                )
                sheet.merge_range(row, 0, row, 6, section_title, fmt_section)
                row += 1

                # Column headers
                headers = ['Date', 'Reference', 'From', 'To', 'IN', 'OUT', 'Balance']
                for col, h in enumerate(headers):
                    sheet.write(row, col, h, fmt_header)
                row += 1

            # Data row
            if line['is_opening']:
                f_text = fmt_opening_text
                f_num = fmt_opening_number
                f_date = fmt_opening_date
            else:
                f_text = fmt_text
                f_num = fmt_number
                f_date = fmt_date_cell

            dt = line['date']
            if isinstance(dt, datetime):
                sheet.write_datetime(row, 0, dt, f_date)
            else:
                sheet.write(row, 0, str(dt), f_text)
            sheet.write(row, 1, line['reference'], f_text)
            sheet.write(row, 2, line['location_from'], f_text)
            sheet.write(row, 3, line['location_to'], f_text)
            sheet.write(row, 4, line['qty_in'], f_num)
            sheet.write(row, 5, line['qty_out'], f_num)
            sheet.write(row, 6, line['balance'], f_num)
            row += 1

        workbook.close()
        output.seek(0)

        filename = 'stock_card_%s.xlsx' % fields.Date.context_today(self).isoformat()
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'raw': output.read(),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        output.close()

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }


class StockCardReportLine(models.TransientModel):
    _name = 'stock.card.report.line'
    _description = 'Stock Card Report Line'

    wizard_id = fields.Many2one('stock.card.report.wizard', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    location_id = fields.Many2one('stock.location', string='Location', readonly=True)
    date = fields.Datetime(string='Date', readonly=True)
    reference = fields.Char(string='Reference', readonly=True)
    location_from = fields.Char(string='From', readonly=True)
    location_to = fields.Char(string='To', readonly=True)
    qty_in = fields.Float(string='IN', readonly=True, digits='Product Unit')
    qty_out = fields.Float(string='OUT', readonly=True, digits='Product Unit')
    balance = fields.Float(string='Balance', readonly=True, digits='Product Unit')
    product_uom = fields.Char(string='UoM', readonly=True)
    is_opening = fields.Boolean(string='Opening Balance', readonly=True)
