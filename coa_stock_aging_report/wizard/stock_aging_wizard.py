# -*- coding: utf-8 -*-
import io
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from collections import defaultdict

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class StockAgingReportWizard(models.TransientModel):
    _name = 'stock.aging.report.wizard'
    _description = 'Stock Aging Report Wizard'

    # ─── Company ──────────────────────────────────────────────────────────────
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    # ─── Report type ──────────────────────────────────────────────────────────
    report_type = fields.Selection([
        ('warehouse', 'By Warehouse'),
        ('location', 'By Location'),
    ], string='Report Type', default='warehouse', required=True)

    # ─── Filters ──────────────────────────────────────────────────────────────
    warehouse_ids = fields.Many2many(
        'stock.warehouse',
        'aging_report_warehouse_rel',
        'wizard_id', 'warehouse_id',
        string='Warehouses',
        help='Leave empty to include all warehouses',
    )
    location_ids = fields.Many2many(
        'stock.location',
        'aging_report_location_rel',
        'wizard_id', 'location_id',
        string='Locations',
        domain=[('usage', '=', 'internal')],
        help='Leave empty to include all internal locations',
    )
    product_ids = fields.Many2many(
        'product.product',
        'aging_report_product_rel',
        'wizard_id', 'product_id',
        string='Products',
        help='Leave empty to include all products',
    )
    categ_ids = fields.Many2many(
        'product.category',
        'aging_report_categ_rel',
        'wizard_id', 'categ_id',
        string='Product Categories',
        help='Leave empty to include all categories',
    )

    # ─── Date & Aging periods ─────────────────────────────────────────────────
    date_to = fields.Date(
        string='As of Date',
        default=fields.Date.today,
        required=True,
    )
    period1 = fields.Integer('Period 1 End (days)', default=30,
        help='Age bucket: 0 to this many days')
    period2 = fields.Integer('Period 2 End (days)', default=60,
        help='Age bucket: Period1+1 to this many days')
    period3 = fields.Integer('Period 3 End (days)', default=90,
        help='Age bucket: Period2+1 to this many days')
    period4 = fields.Integer('Period 4 End (days)', default=120,
        help='Age bucket: Period3+1 to this many days')

    # ─── Onchange ─────────────────────────────────────────────────────────────
    @api.onchange('report_type')
    def _onchange_report_type(self):
        self.warehouse_ids = False
        self.location_ids = False

    @api.constrains('period1', 'period2', 'period3', 'period4')
    def _check_periods(self):
        for rec in self:
            if not (0 < rec.period1 < rec.period2 < rec.period3 < rec.period4):
                raise UserError(_(
                    'Aging periods must be in ascending order: '
                    'Period1 < Period2 < Period3 < Period4'
                ))

    # ─── Action: Print PDF ────────────────────────────────────────────────────
    def action_print_report(self):
        self.ensure_one()
        data = self._build_report_data()
        if not data.get('groups'):
            raise UserError(_('No stock data found for the selected filters.'))
        return self.env.ref(
            'coa_stock_aging_report.action_stock_aging_report'
        ).report_action(self, data=data)

    # ─── Action: Export Excel ─────────────────────────────────────────────────
    def action_export_excel(self):
        self.ensure_one()
        if not xlsxwriter:
            raise UserError(_('The xlsxwriter library is required to export Excel files.'))
        data = self._build_report_data()
        if not data.get('groups'):
            raise UserError(_('No stock data found for the selected filters.'))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Stock Aging Report')

        # ── Formats ───────────────────────────────────────────────────────────
        fmt_title = workbook.add_format({
            'bold': True, 'font_size': 16, 'align': 'center',
            'font_color': '#1a6496',
        })
        fmt_subtitle = workbook.add_format({
            'bold': True, 'font_size': 11, 'align': 'center',
        })
        fmt_company = workbook.add_format({
            'font_size': 10, 'align': 'center', 'italic': True,
            'font_color': '#666666',
        })
        fmt_group = workbook.add_format({
            'bold': True, 'font_size': 11,
            'bg_color': '#e8f4f8', 'font_color': '#1a6496',
            'left': 4, 'left_color': '#1a6496', 'border': 1,
        })
        fmt_header = workbook.add_format({
            'bold': True, 'font_size': 10,
            'bg_color': '#d9edf7', 'border': 1, 'align': 'center',
            'text_wrap': True,
        })
        fmt_text = workbook.add_format({'font_size': 10, 'border': 1})
        fmt_num = workbook.add_format({
            'font_size': 10, 'border': 1,
            'num_format': '#,##0.00', 'align': 'right',
        })
        fmt_num_zero = workbook.add_format({
            'font_size': 10, 'border': 1,
            'num_format': '#,##0.00', 'align': 'right',
            'font_color': '#aaaaaa',
        })
        fmt_subtotal = workbook.add_format({
            'bold': True, 'font_size': 10,
            'bg_color': '#dff0d8', 'border': 1,
            'num_format': '#,##0.00', 'align': 'right',
        })
        fmt_subtotal_text = workbook.add_format({
            'bold': True, 'font_size': 10,
            'bg_color': '#dff0d8', 'border': 1,
        })
        fmt_grand = workbook.add_format({
            'bold': True, 'font_size': 11,
            'bg_color': '#1a6496', 'font_color': 'white',
            'border': 1, 'num_format': '#,##0.00', 'align': 'right',
        })
        fmt_grand_text = workbook.add_format({
            'bold': True, 'font_size': 11,
            'bg_color': '#1a6496', 'font_color': 'white', 'border': 1,
        })

        col_headers = data['col_headers']
        # columns: Product | Category | UoM | [5 buckets] | Total Qty | Total Value
        ncols = 3 + len(col_headers) + 2  # = 10

        # Column widths
        sheet.set_column(0, 0, 35)   # Product
        sheet.set_column(1, 1, 22)   # Category
        sheet.set_column(2, 2, 10)   # UoM
        for i in range(len(col_headers)):
            sheet.set_column(3 + i, 3 + i, 14)
        sheet.set_column(3 + len(col_headers), 3 + len(col_headers), 14)      # Total Qty
        sheet.set_column(3 + len(col_headers) + 1, 3 + len(col_headers) + 1, 18)  # Total Value

        row = 0
        # ── Header ────────────────────────────────────────────────────────────
        sheet.merge_range(row, 0, row, ncols - 1, 'Stock Aging Report', fmt_title)
        row += 1
        sheet.merge_range(row, 0, row, ncols - 1,
            '%s  |  As of: %s' % (data['report_type'], data['date_to']), fmt_subtitle)
        row += 1
        sheet.merge_range(row, 0, row, ncols - 1, data['company_name'], fmt_company)
        row += 2

        cur = data['currency']
        cur_pos = data['currency_position']

        def fmt_value(v):
            return ('%s %s' % (cur, '{:,.2f}'.format(v))) if cur_pos == 'before' \
                else ('%s %s' % ('{:,.2f}'.format(v), cur))

        for group in data['groups']:
            # Group header
            sheet.merge_range(row, 0, row, ncols - 1, group['name'], fmt_group)
            row += 1

            # Column headers
            headers = ['Product', 'Category', 'UoM'] + \
                      [h + ' days' for h in col_headers] + \
                      ['Total Qty', 'Total Value']
            for c, h in enumerate(headers):
                sheet.write(row, c, h, fmt_header)
            row += 1

            # Data rows
            for line in group['lines']:
                sheet.write(row, 0, line['product'], fmt_text)
                sheet.write(row, 1, line['category'], fmt_text)
                sheet.write(row, 2, line['uom'], fmt_text)
                for i, q in enumerate(line['qty']):
                    f = fmt_num if q > 0.0009 else fmt_num_zero
                    sheet.write(row, 3 + i, q, f)
                sheet.write(row, 3 + len(col_headers), line['total_qty'], fmt_num)
                sheet.write(row, 3 + len(col_headers) + 1, line['total_value'], fmt_num)
                row += 1

            # Subtotal row
            sub = group['subtotal']
            sheet.merge_range(row, 0, row, 2,
                'Subtotal – %s' % group['name'], fmt_subtotal_text)
            for i, q in enumerate(sub['qty']):
                sheet.write(row, 3 + i, q, fmt_subtotal)
            sheet.write(row, 3 + len(col_headers), sub['total_qty'], fmt_subtotal)
            sheet.write(row, 3 + len(col_headers) + 1, sub['total_value'], fmt_subtotal)
            row += 2  # blank line between groups

        # Grand total row
        grand = data['grand']
        sheet.merge_range(row, 0, row, 2, 'GRAND TOTAL', fmt_grand_text)
        for i, q in enumerate(grand['qty']):
            sheet.write(row, 3 + i, q, fmt_grand)
        sheet.write(row, 3 + len(col_headers), grand['total_qty'], fmt_grand)
        sheet.write(row, 3 + len(col_headers) + 1, grand['total_value'], fmt_grand)
        row += 2

        # Footer
        fmt_footer = workbook.add_format({'font_size': 8, 'italic': True, 'font_color': '#888888'})
        sheet.merge_range(row, 0, row, ncols - 1,
            '* Quantities calculated using FIFO. Values use unit cost at time of receipt. '
            'Generated: %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            fmt_footer)

        workbook.close()
        output.seek(0)

        filename = 'stock_aging_%s.xlsx' % data['date_to']
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

    # ─── Core: build report data ──────────────────────────────────────────────
    def _build_report_data(self):
        """Return a dict consumed by the QWeb PDF template."""
        self.ensure_one()

        locations = self._get_internal_locations()
        products   = self._get_products()
        date_to    = self.date_to
        today      = date_to  # alias

        p1, p2, p3, p4 = self.period1, self.period2, self.period3, self.period4

        # Column headers for the template
        col_headers = [
            f'0 – {p1}',
            f'{p1+1} – {p2}',
            f'{p2+1} – {p3}',
            f'{p3+1} – {p4}',
            f'> {p4}',
        ]

        # Group by grouping_label (warehouse name or location name)
        group_map = self._get_group_map(locations)  # location.id -> group_label

        # We'll collect data: {(group_label, product_id): {buckets…}}
        aggregated = defaultdict(lambda: {
            'qty': [0.0] * 5,
            'value': [0.0] * 5,
            'product': None,
            'category': '',
            'uom': '',
        })

        for product in products:
            product_locations = locations  # all; filter per product below

            # Compute FIFO batches remaining for this product across all locations
            batches = self._compute_fifo_batches(product, locations, date_to)

            for batch in batches:
                loc_id   = batch['location_id']
                batch_date = batch['date']
                qty      = batch['qty']
                value    = batch['value']

                batch_day = batch_date.date() if isinstance(batch_date, datetime) else batch_date
                age = (today - batch_day).days
                bucket_idx = self._get_bucket_index(age, p1, p2, p3, p4)

                group_label = group_map.get(loc_id, _('Unknown'))
                key = (group_label, product.id)

                agg = aggregated[key]
                agg['qty'][bucket_idx]   += qty
                agg['value'][bucket_idx] += value
                agg['product']   = product.display_name
                agg['category']  = product.categ_id.complete_name or ''
                agg['uom']       = product.uom_id.name or ''

        # ── Build per-group ordered structure ─────────────────────────────────
        # groups_data: [ {name, lines:[...], subtotal_qty:[...], ...} ]
        group_order = []
        group_lines = defaultdict(list)
        group_subtotals = defaultdict(lambda: {
            'qty': [0.0]*5, 'value': [0.0]*5,
            'total_qty': 0.0, 'total_value': 0.0,
        })

        for (group_label, product_id), agg in sorted(
            aggregated.items(), key=lambda x: (x[0][0], x[0][1])
        ):
            total_qty   = sum(agg['qty'])
            total_value = sum(agg['value'])
            if total_qty <= 0:
                continue

            line = {
                'product':     agg['product'],
                'category':    agg['category'],
                'uom':         agg['uom'],
                'qty':         agg['qty'],
                'value':       agg['value'],
                'total_qty':   total_qty,
                'total_value': total_value,
            }
            group_lines[group_label].append(line)
            if group_label not in group_order:
                group_order.append(group_label)

            g = group_subtotals[group_label]
            for i in range(5):
                g['qty'][i]   += agg['qty'][i]
                g['value'][i] += agg['value'][i]
            g['total_qty']   += total_qty
            g['total_value'] += total_value

        # Build groups list for template
        groups = []
        for gname in group_order:
            groups.append({
                'name':     gname,
                'lines':    group_lines[gname],
                'subtotal': group_subtotals[gname],
            })

        # Grand totals
        grand = {'qty': [0.0]*5, 'value': [0.0]*5, 'total_qty': 0.0, 'total_value': 0.0}
        for g in group_subtotals.values():
            for i in range(5):
                grand['qty'][i]   += g['qty'][i]
                grand['value'][i] += g['value'][i]
            grand['total_qty']   += g['total_qty']
            grand['total_value'] += g['total_value']

        currency = self.company_id.currency_id

        return {
            'wizard_id':         self.id,
            'report_type':       dict(self._fields['report_type'].selection)[self.report_type],
            'date_to':           fields.Date.to_string(date_to),
            'col_headers':       col_headers,
            'groups':            groups,
            'grand':             grand,
            'currency':          currency.symbol,
            'currency_position': currency.position,
            'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4,
            'company_name':       self.company_id.name,
        }

    # ─── FIFO batch computation ───────────────────────────────────────────────
    def _compute_fifo_batches(self, product, locations, date_to):
        """
        Apply a FIFO algorithm across stock move lines to determine
        which 'batches' of stock are still on hand and their arrival dates.

        Returns list of dicts: {location_id, date, qty, value}
        """
        location_ids = set(locations.ids)
        date_to_dt   = datetime.combine(date_to, datetime.max.time())

        self.env.cr.execute("""
            SELECT
                sml.location_dest_id   AS loc_id,
                sml.date               AS move_date,
                SUM(sml.quantity)      AS qty_in,
                COALESCE(AVG(sm.price_unit), 0) AS unit_cost
            FROM stock_move_line sml
            JOIN stock_move sm ON sm.id = sml.move_id
            WHERE sml.product_id = %s
              AND sml.state = 'done'
              AND sml.date <= %s
              AND sml.location_dest_id = ANY(%s)
              AND (sml.location_id != ALL(%s)
                   OR sml.location_id = sml.location_dest_id)
            GROUP BY sml.location_dest_id, sml.date, sm.price_unit
            ORDER BY sml.date ASC
        """, (product.id, date_to_dt, list(location_ids), list(location_ids)))
        incoming_rows = self.env.cr.fetchall()

        self.env.cr.execute("""
            SELECT
                sml.location_id        AS loc_id,
                SUM(sml.quantity)      AS qty_out
            FROM stock_move_line sml
            WHERE sml.product_id = %s
              AND sml.state = 'done'
              AND sml.date <= %s
              AND sml.location_id = ANY(%s)
              AND (sml.location_dest_id != ALL(%s)
                   OR sml.location_id = sml.location_dest_id)
            GROUP BY sml.location_id
        """, (product.id, date_to_dt, list(location_ids), list(location_ids)))
        outgoing_map = {row[0]: row[1] for row in self.env.cr.fetchall()}

        # Build FIFO per location
        result = []
        # Group incoming by location
        loc_incoming = defaultdict(list)
        for loc_id, move_date, qty_in, unit_cost in incoming_rows:
            loc_incoming[loc_id].append([move_date, qty_in, unit_cost])

        for loc_id, batches in loc_incoming.items():
            remaining_out = outgoing_map.get(loc_id, 0.0)
            for batch in batches:
                move_date, qty, unit_cost = batch
                if remaining_out >= qty:
                    remaining_out -= qty
                    continue
                remaining_qty = qty - remaining_out
                remaining_out = 0.0
                if remaining_qty > 0.0001:
                    result.append({
                        'location_id': loc_id,
                        'date': move_date,
                        'qty': remaining_qty,
                        'value': remaining_qty * unit_cost,
                    })

        return result

    # ─── Helpers ──────────────────────────────────────────────────────────────
    def _get_bucket_index(self, age, p1, p2, p3, p4):
        if age <= p1:
            return 0
        elif age <= p2:
            return 1
        elif age <= p3:
            return 2
        elif age <= p4:
            return 3
        else:
            return 4

    def _get_internal_locations(self):
        """Return stock.location recordset based on wizard settings."""
        if self.report_type == 'warehouse':
            warehouses = self.warehouse_ids or self.env['stock.warehouse'].search(
                [('company_id', '=', self.company_id.id)]
            )
            locations = self.env['stock.location']
            for wh in warehouses:
                locations |= self.env['stock.location'].search([
                    ('id', 'child_of', wh.lot_stock_id.id),
                    ('usage', '=', 'internal'),
                    ('active', '=', True),
                ])
            return locations
        else:
            if self.location_ids:
                # Include children of selected locations
                all_locs = self.env['stock.location']
                for loc in self.location_ids:
                    all_locs |= self.env['stock.location'].search([
                        ('id', 'child_of', loc.id),
                        ('usage', '=', 'internal'),
                        ('active', '=', True),
                    ])
                return all_locs
            return self.env['stock.location'].search([
                ('usage', '=', 'internal'),
                ('active', '=', True),
                ('company_id', '=', self.company_id.id),
            ])

    def _get_products(self):
        """Return product.product recordset based on wizard filters."""
        domain = [('is_storable', '=', True)]
        if self.product_ids:
            domain += [('id', 'in', self.product_ids.ids)]
        elif self.categ_ids:
            domain += [('categ_id', 'in', self.categ_ids.ids)]
        return self.env['product.product'].search(domain)

    def _get_group_map(self, locations):
        """Return {location_id: group_label} based on report_type."""
        group_map = {}
        if self.report_type == 'warehouse':
            warehouses = self.warehouse_ids or self.env['stock.warehouse'].search(
                [('company_id', '=', self.company_id.id)]
            )
            for wh in warehouses:
                wh_locs = self.env['stock.location'].search([
                    ('id', 'child_of', wh.lot_stock_id.id),
                    ('usage', '=', 'internal'),
                ])
                for loc in wh_locs:
                    group_map[loc.id] = wh.name
        else:
            for loc in locations:
                group_map[loc.id] = loc.complete_name or loc.name
        return group_map
