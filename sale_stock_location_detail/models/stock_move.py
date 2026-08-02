from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_product_location_detail(self, product):
        """يرجع نص تفاصيل المخازن لمنتج معين من الـ moves الخاصة بهذا الـ picking"""
        moves = self.move_ids.filtered(lambda m: m.product_id == product and m.state == 'done')
        parts = []
        for move in moves:
            text = move._get_location_detail_text()
            if text:
                parts.append(text)
        return '\n'.join(parts)


class StockMove(models.Model):
    _inherit = 'stock.move'

    reserved_location_detail = fields.Char(
        string='Location Detail',
        compute='_compute_reserved_location_detail',
        store=False,
        help='Sub-locations and quantities from Detailed Operations',
    )

    @api.depends('move_line_ids', 'move_line_ids.location_id',
                 'move_line_ids.lot_id', 'move_line_ids.quantity', 'state')
    def _compute_reserved_location_detail(self):
        for move in self:
            move.reserved_location_detail = move._get_location_detail_text()

    def _get_location_detail_text(self):
        """
        يجمع الكميات per (location, lot) من move_line_ids
        ويرجع نص ملخص
        """
        move_lines = self.move_line_ids.filtered(
            lambda ml: ml.quantity > 0
        )
        if not move_lines:
            return ''

        location_qty = {}
        for ml in move_lines:
            loc = ml.location_id.complete_name or ml.location_id.name
            lot = ml.lot_id.name if ml.lot_id else ''
            key = loc + (f'  [{lot}]' if lot else '')
            location_qty[key] = location_qty.get(key, 0) + ml.quantity

        parts = [f'{loc}  ×{qty:g}' for loc, qty in location_qty.items()]
        return '\n'.join(parts)
