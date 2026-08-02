from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    actual_reserved_qty = fields.Float(
        string='Actual Reserved Qty',
        compute='_compute_actual_reserved_qty',
        store=False,
        help='Actual reserved quantity from move lines'
    )

    def _compute_actual_reserved_qty(self):
        for move in self:
            move.actual_reserved_qty = sum(move.move_line_ids.mapped('quantity'))

    def action_un_reserve(self):
        for move in self.filtered(lambda m: m.state == 'assigned'):
            move._do_unreserve()
        return {'type': 'ir.actions.act_window_close'}
