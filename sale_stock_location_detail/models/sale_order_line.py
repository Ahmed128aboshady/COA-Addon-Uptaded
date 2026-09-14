from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # ─────────────────────────────────────────────────────────────────
    # Computed (real-time): من الـ reserved move lines مباشرة
    # يتحدث لحظياً - مش مخزّن
    # ─────────────────────────────────────────────────────────────────
    reserved_location_detail = fields.Char(
        string='Reserved From',
        compute='_compute_reserved_location_detail',
        store=False,
        help='Sub-locations and quantities as reserved by Odoo (Detailed Operations)',
    )

    # ─────────────────────────────────────────────────────────────────
    # Stored: بيتخزن عشان يظهر في الـ invoice والـ print
    # بيتملى لما يتعمل Confirm أو Reserve
    # ─────────────────────────────────────────────────────────────────
    reserved_location_stored = fields.Char(
        string='Source Location Detail',
        store=True,
        copy=False,
        readonly=True,
    )

    # ─────────────────────────────────────────────────────────────────
    def _get_reserved_location_text(self):
        """
        بيجيب الـ stock.move.line المرتبطة بالـ SO line دي
        سواء reserved أو done - ويرجع نص ملخص
        """
        move_lines = self.env['stock.move.line'].search([
            ('move_id.sale_line_id', '=', self.id),
            ('state', 'in', ['assigned', 'partially_available', 'done']),
        ])

        if not move_lines:
            return ''

        # نجمع الكمية per (location, lot)
        location_qty = {}
        for ml in move_lines:
            loc = ml.location_id.complete_name or ml.location_id.name
            lot = ml.lot_id.name if ml.lot_id else ''
            # في Odoo 18 الحقلان qty_done و reserved_uom_qty اندمجا في quantity
            qty = ml.quantity

            if qty <= 0:
                continue

            key = loc + (f'  [{lot}]' if lot else '')
            location_qty[key] = location_qty.get(key, 0) + qty

        if not location_qty:
            return ''

        parts = [f'{loc}  ×{qty:g}' for loc, qty in location_qty.items()]
        return '\n'.join(parts)

    def _compute_reserved_location_detail(self):
        for line in self:
            line.reserved_location_detail = line._get_reserved_location_text()

    def _refresh_stored_location_detail(self):
        """يُستدعى بعد Reserve أو Confirm لتخزين التفاصيل"""
        for line in self:
            text = line._get_reserved_location_text()
            if text:
                line.reserved_location_stored = text


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """بعد الـ Confirm وإنشاء الـ moves، نخزّن الـ location details"""
        res = super().action_confirm()
        # نستنى إن الـ reserve يحصل (لو auto)
        for order in self:
            order.order_line._refresh_stored_location_detail()
        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_assign(self):
        """بعد Reserve (Check Availability)، نحدّث الـ stored detail"""
        res = super().action_assign()
        sale_lines = self.move_ids.mapped('sale_line_id')
        sale_lines._refresh_stored_location_detail()
        return res
