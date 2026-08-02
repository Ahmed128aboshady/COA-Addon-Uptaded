# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ===== التصنيع =====
    tracking_manufactured_value = fields.Monetary(
        string='قيمة المُصنَّع',
        compute='_compute_tracking_values', store=True,
        currency_field='currency_id',
        help="قيمة ما تم تصنيعه بسعر البيع (نسبة الإنتاج × قيمة السطر).",
    )
    tracking_to_manufacture_value = fields.Monetary(
        string='المتبقي للتصنيع',
        compute='_compute_tracking_values', store=True,
        currency_field='currency_id',
    )

    # ===== التسليم =====
    tracking_delivered_value = fields.Monetary(
        string='قيمة المُسلَّم',
        compute='_compute_tracking_values', store=True,
        currency_field='currency_id',
    )
    tracking_to_deliver_value = fields.Monetary(
        string='المتبقي للتسليم',
        compute='_compute_tracking_values', store=True,
        currency_field='currency_id',
    )

    # ===== الفوترة =====
    tracking_invoiced_value = fields.Monetary(
        string='قيمة المُفوتَر',
        compute='_compute_tracking_values', store=True,
        currency_field='currency_id',
    )
    tracking_to_invoice_value = fields.Monetary(
        string='المتبقي للفوترة',
        compute='_compute_tracking_values', store=True,
        currency_field='currency_id',
    )

    # ===== Dashboard data method =====
    @api.model
    def get_so_tracking_data(self, date_from=None, date_to=None, state='all'):
        """Returns structured SO tracking data for the OWL dashboard.
        Quantities only — manufacturing / delivery / invoicing per line."""
        domain = [('state', 'not in', ('draft', 'sent', 'cancel'))]
        if state and state != 'all':
            domain.append(('state', '=', state))
        if date_from:
            domain.append(('date_order', '>=', date_from + ' 00:00:00'))
        if date_to:
            domain.append(('date_order', '<=', date_to + ' 23:59:59'))

        orders = self.search(domain, order='date_order desc')

        # Batch-load MOs for all lines at once (avoids N+1 queries)
        product_lines = orders.mapped('order_line').filtered(
            lambda l: not l.display_type)
        all_line_ids = product_lines.ids

        productions = (
            self.env['mrp.production'].search([
                ('sale_line_id', 'in', all_line_ids),
                ('state', '!=', 'cancel'),
            ]) if all_line_ids else self.env['mrp.production']
        )
        # Index MOs by sale.order.line id
        mfg_by_line = {}
        for mo in productions:
            lid = mo.sale_line_id.id
            mfg_by_line.setdefault(lid, []).append(mo)

        result = []
        for order in orders:
            lines_data = []
            for line in order.order_line:
                if line.display_type:
                    continue

                ordered_qty = line.product_uom_qty or 0.0

                # Manufactured qty from linked MOs
                manufactured_qty = 0.0
                for mo in mfg_by_line.get(line.id, []):
                    mo_qty = (getattr(mo, 'qty_produced', None) or
                              (mo.product_qty if mo.state == 'done' else 0.0))
                    if (mo.product_uom_id and line.product_uom_id
                            and mo.product_uom_id != line.product_uom_id):
                        mo_qty = mo.product_uom_id._compute_quantity(
                            mo_qty, line.product_uom_id)
                    manufactured_qty += mo_qty
                manufactured_qty = min(manufactured_qty, ordered_qty)

                delivered_qty = line.qty_delivered or 0.0
                invoiced_qty  = line.qty_invoiced or 0.0

                lines_data.append({
                    'id':           line.id,
                    'product_name': line.product_id.display_name or line.name or '',
                    'uom':          line.product_uom_id.name if line.product_uom_id else '',
                    'ordered_qty':  ordered_qty,
                    'manufactured_qty':   manufactured_qty,
                    'to_manufacture_qty': max(ordered_qty - manufactured_qty, 0.0),
                    'delivered_qty':  delivered_qty,
                    'to_deliver_qty': max(ordered_qty - delivered_qty, 0.0),
                    'invoiced_qty':   invoiced_qty,
                    'to_invoice_qty': max(ordered_qty - invoiced_qty, 0.0),
                })

            result.append({
                'id':      order.id,
                'name':    order.name,
                'partner': order.partner_id.name or '',
                'date':    (order.date_order.strftime('%Y-%m-%d')
                            if order.date_order else ''),
                'state':   order.state,
                'lines':   lines_data,
                # Totals
                'total_ordered_qty':
                    sum(l['ordered_qty'] for l in lines_data),
                'total_manufactured_qty':
                    sum(l['manufactured_qty'] for l in lines_data),
                'total_to_manufacture_qty':
                    sum(l['to_manufacture_qty'] for l in lines_data),
                'total_delivered_qty':
                    sum(l['delivered_qty'] for l in lines_data),
                'total_to_deliver_qty':
                    sum(l['to_deliver_qty'] for l in lines_data),
                'total_invoiced_qty':
                    sum(l['invoiced_qty'] for l in lines_data),
                'total_to_invoice_qty':
                    sum(l['to_invoice_qty'] for l in lines_data),
            })

        return result

    # ===== Excel export =====
    @api.model
    def export_so_tracking_excel(self, date_from=None, date_to=None, state='all'):
        """Generate a two-sheet Excel workbook with SO tracking data."""
        import io
        import base64
        import xlsxwriter

        data = self.get_so_tracking_data(date_from, date_to, state)

        output = io.BytesIO()
        wb = xlsxwriter.Workbook(output, {'in_memory': True})

        # ── Format definitions ──────────────────────────────────────────────
        def _hdr(color):
            return wb.add_format({
                'bold': True, 'bg_color': color, 'font_color': '#FFFFFF',
                'align': 'center', 'valign': 'vcenter',
                'border': 1, 'font_size': 11,
            })

        def _sub(color):
            return wb.add_format({
                'bold': True, 'bg_color': color, 'font_color': '#FFFFFF',
                'align': 'center', 'border': 1, 'font_size': 10,
            })

        fmt_main  = _hdr('#714B9A')
        fmt_mfg   = _hdr('#5a3d7e')
        fmt_dlv   = _hdr('#1565c0')
        fmt_inv   = _hdr('#2e7d32')
        fmt_smfg  = _sub('#7e57c2')
        fmt_sdlv  = _sub('#1976d2')
        fmt_sinv  = _sub('#388e3c')

        fmt_cell  = wb.add_format({'border': 1, 'font_size': 10})
        fmt_bold  = wb.add_format({'bold': True, 'border': 1, 'font_size': 10})
        fmt_num   = wb.add_format({'border': 1, 'num_format': '#,##0.##', 'font_size': 10})
        fmt_warn  = wb.add_format({'border': 1, 'num_format': '#,##0.##',
                                    'font_color': '#c62828', 'bold': True, 'font_size': 10})
        fmt_done  = wb.add_format({'border': 1, 'num_format': '#,##0.##',
                                    'font_color': '#2e7d32', 'bold': True, 'font_size': 10})
        fmt_total = wb.add_format({'bold': True, 'bg_color': '#ede8f7',
                                    'border': 1, 'num_format': '#,##0.##', 'font_size': 10})

        state_labels = {
            'sale': 'مؤكد', 'done': 'مغلق',
            'draft': 'مسودة', 'sent': 'مرسل', 'cancel': 'ملغي',
        }

        # ══════════════════════════════════════════════════════════════════
        # Sheet 1 — SO Summary
        # ══════════════════════════════════════════════════════════════════
        ws1 = wb.add_worksheet('ملخص أوامر البيع')
        ws1.right_to_left()
        ws1.set_zoom(90)
        ws1.freeze_panes(2, 0)

        # Row 0 — group headers
        ws1.merge_range('A1:A2', 'أمر البيع',  fmt_main)
        ws1.merge_range('B1:B2', 'العميل',     fmt_main)
        ws1.merge_range('C1:C2', 'التاريخ',    fmt_main)
        ws1.merge_range('D1:D2', 'الحالة',     fmt_main)
        ws1.merge_range('E1:E2', 'عدد الأصناف', fmt_main)
        ws1.merge_range('F1:G1', 'التصنيع (كمية)', fmt_mfg)
        ws1.merge_range('H1:I1', 'التسليم (كمية)',  fmt_dlv)
        ws1.merge_range('J1:K1', 'الفوترة (كمية)',  fmt_inv)

        # Row 1 — sub-headers
        ws1.write('F2', 'تم',     fmt_smfg)
        ws1.write('G2', 'متبقي',  fmt_smfg)
        ws1.write('H2', 'تم',     fmt_sdlv)
        ws1.write('I2', 'متبقي',  fmt_sdlv)
        ws1.write('J2', 'تم',     fmt_sinv)
        ws1.write('K2', 'متبقي',  fmt_sinv)

        # Column widths
        ws1.set_column('A:A', 14)
        ws1.set_column('B:B', 22)
        ws1.set_column('C:C', 12)
        ws1.set_column('D:D', 10)
        ws1.set_column('E:E', 11)
        ws1.set_column('F:K', 13)

        r = 2
        for so in data:
            ws1.write(r, 0, so['name'],                          fmt_bold)
            ws1.write(r, 1, so['partner'],                       fmt_cell)
            ws1.write(r, 2, so['date'],                          fmt_cell)
            ws1.write(r, 3, state_labels.get(so['state'], so['state']), fmt_cell)
            ws1.write(r, 4, len(so['lines']),                    fmt_num)
            # MFG
            mfg_done = so['total_manufactured_qty']
            mfg_rem  = so['total_to_manufacture_qty']
            ws1.write(r, 5, mfg_done, fmt_done if mfg_rem == 0 and mfg_done > 0 else fmt_num)
            ws1.write(r, 6, mfg_rem,  fmt_warn if mfg_rem > 0 else fmt_num)
            # DLV
            dlv_done = so['total_delivered_qty']
            dlv_rem  = so['total_to_deliver_qty']
            ws1.write(r, 7, dlv_done, fmt_done if dlv_rem == 0 and dlv_done > 0 else fmt_num)
            ws1.write(r, 8, dlv_rem,  fmt_warn if dlv_rem > 0 else fmt_num)
            # INV
            inv_done = so['total_invoiced_qty']
            inv_rem  = so['total_to_invoice_qty']
            ws1.write(r, 9,  inv_done, fmt_done if inv_rem == 0 and inv_done > 0 else fmt_num)
            ws1.write(r, 10, inv_rem,  fmt_warn if inv_rem > 0 else fmt_num)
            r += 1

        # Totals row
        if data:
            ws1.write(r, 0, 'الإجمالي', fmt_total)
            ws1.write(r, 1, '',          fmt_total)
            ws1.write(r, 2, '',          fmt_total)
            ws1.write(r, 3, '',          fmt_total)
            ws1.write(r, 4, sum(len(s['lines']) for s in data), fmt_total)
            ws1.write(r, 5, sum(s['total_manufactured_qty']    for s in data), fmt_total)
            ws1.write(r, 6, sum(s['total_to_manufacture_qty']  for s in data), fmt_total)
            ws1.write(r, 7, sum(s['total_delivered_qty']       for s in data), fmt_total)
            ws1.write(r, 8, sum(s['total_to_deliver_qty']      for s in data), fmt_total)
            ws1.write(r, 9, sum(s['total_invoiced_qty']        for s in data), fmt_total)
            ws1.write(r, 10, sum(s['total_to_invoice_qty']     for s in data), fmt_total)

        # ══════════════════════════════════════════════════════════════════
        # Sheet 2 — Line Details
        # ══════════════════════════════════════════════════════════════════
        ws2 = wb.add_worksheet('تفاصيل الأصناف')
        ws2.right_to_left()
        ws2.set_zoom(90)
        ws2.freeze_panes(1, 0)

        detail_headers = [
            ('أمر البيع',    14, fmt_main),
            ('العميل',       22, fmt_main),
            ('المنتج',       30, fmt_main),
            ('الوحدة',       10, fmt_main),
            ('الكمية المطلوبة', 14, fmt_main),
            ('تصنيع تم',    13, fmt_mfg),
            ('تصنيع متبقي', 13, fmt_mfg),
            ('تسليم تم',    13, fmt_dlv),
            ('تسليم متبقي', 13, fmt_dlv),
            ('فوترة تم',    13, fmt_inv),
            ('فوترة متبقي', 13, fmt_inv),
        ]
        for col, (title, width, fmt) in enumerate(detail_headers):
            ws2.write(0, col, title, fmt)
            ws2.set_column(col, col, width)

        r2 = 1
        for so in data:
            for line in so['lines']:
                ws2.write(r2, 0,  so['name'],            fmt_bold)
                ws2.write(r2, 1,  so['partner'],          fmt_cell)
                ws2.write(r2, 2,  line['product_name'],   fmt_cell)
                ws2.write(r2, 3,  line['uom'],            fmt_cell)
                ws2.write(r2, 4,  line['ordered_qty'],    fmt_num)
                # MFG
                m_d = line['manufactured_qty']
                m_r = line['to_manufacture_qty']
                ws2.write(r2, 5, m_d, fmt_done if m_r == 0 and m_d > 0 else fmt_num)
                ws2.write(r2, 6, m_r, fmt_warn if m_r > 0 else fmt_num)
                # DLV
                d_d = line['delivered_qty']
                d_r = line['to_deliver_qty']
                ws2.write(r2, 7, d_d, fmt_done if d_r == 0 and d_d > 0 else fmt_num)
                ws2.write(r2, 8, d_r, fmt_warn if d_r > 0 else fmt_num)
                # INV
                i_d = line['invoiced_qty']
                i_r = line['to_invoice_qty']
                ws2.write(r2, 9,  i_d, fmt_done if i_r == 0 and i_d > 0 else fmt_num)
                ws2.write(r2, 10, i_r, fmt_warn if i_r > 0 else fmt_num)
                r2 += 1

        wb.close()
        output.seek(0)

        file_b64 = base64.b64encode(output.read()).decode('utf-8')
        fname = 'SO_Tracking'
        if date_from:
            fname += f'_{date_from}'
        if date_to:
            fname += f'_{date_to}'
        fname += '.xlsx'

        return {'filename': fname, 'file_data': file_b64}

    def _get_line_manufactured_ratio(self, line):
        """نسبة ما تم تصنيعه من كمية السطر (0..1).
        MTO مستوى واحد: الربط عبر sale_line_id مضمون."""
        product = line.product_id
        if not product or product.type not in ('consu', 'product'):
            return 0.0
        productions = self.env['mrp.production'].search([
            ('sale_line_id', '=', line.id),
            ('state', '!=', 'cancel'),
        ])
        if not productions:
            return 0.0

        ordered_qty = line.product_uom_qty or 0.0
        if ordered_qty <= 0:
            return 0.0
        produced = 0.0
        for mo in productions:
            # الكمية المنتَجة بوحدة أمر التصنيع، محوّلة لوحدة سطر البيع
            mo_qty = mo.qty_produced if 'qty_produced' in mo._fields else (
                mo.product_qty if mo.state == 'done' else 0.0)
            if mo.product_uom_id and line.product_uom_id \
                    and mo.product_uom_id != line.product_uom_id:
                mo_qty = mo.product_uom_id._compute_quantity(
                    mo_qty, line.product_uom_id)
            produced += mo_qty
        ratio = produced / ordered_qty
        return min(max(ratio, 0.0), 1.0)

    @api.depends(
        'order_line.price_subtotal',
        'order_line.product_uom_qty',
        'order_line.qty_delivered',
        'order_line.qty_invoiced',
        'order_line.product_id',
        'state',
    )
    def _compute_tracking_values(self):
        for order in self:
            manufactured = to_manufacture = 0.0
            delivered = to_deliver = 0.0
            invoiced = to_invoice = 0.0

            for line in order.order_line:
                if line.display_type:
                    continue  # سطور الملاحظات/الأقسام
                qty = line.product_uom_qty or 0.0
                line_value = line.price_subtotal  # قيمة السطر بدون ضريبة
                unit_value = (line_value / qty) if qty else 0.0

                # ---- الفوترة ----
                inv_val = unit_value * (line.qty_invoiced or 0.0)
                invoiced += inv_val
                to_invoice += max(line_value - inv_val, 0.0)

                # ---- التسليم ----
                deliv_val = unit_value * (line.qty_delivered or 0.0)
                delivered += deliv_val
                to_deliver += max(line_value - deliv_val, 0.0)

                # ---- التصنيع ----
                ratio = order._get_line_manufactured_ratio(line)
                man_val = line_value * ratio
                manufactured += man_val
                to_manufacture += max(line_value - man_val, 0.0)

            order.tracking_manufactured_value = manufactured
            order.tracking_to_manufacture_value = to_manufacture
            order.tracking_delivered_value = delivered
            order.tracking_to_deliver_value = to_deliver
            order.tracking_invoiced_value = invoiced
            order.tracking_to_invoice_value = to_invoice


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def write(self, vals):
        res = super().write(vals)
        # عند تغيّر الكمية المنتَجة أو الحالة، أعد حساب مؤشرات الأمر المرتبط
        if vals.keys() & {'qty_producing', 'qty_produced', 'state',
                          'product_qty'}:
            orders = self.env['sale.order']
            for production in self:
                if production.sale_line_id:
                    orders |= production.sale_line_id.order_id
            if orders:
                orders._compute_tracking_values()
        return res
