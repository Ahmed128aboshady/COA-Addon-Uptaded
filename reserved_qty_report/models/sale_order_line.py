from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    reserved_qty = fields.Float(
        string='Reserved Quantity',
        compute='_compute_reserved_qty',
        store=True,
        help='Quantity reserved in stock moves related to this order line'
    )

    @api.depends('product_uom_qty', 'order_id')
    def _compute_reserved_qty(self):
        for line in self:
            # Search for stock moves linked to this sale order line
            moves = self.env['stock.move'].search_read(
                domain=[
                    ('sale_line_id', '=', line.id),
                    ('state', '=', 'assigned'),
                ],
                fields=['product_uom_qty']
            )
            # product_uom_qty in assigned moves is the reserved quantity
            line.reserved_qty = sum(m.get('product_uom_qty', 0) or 0 for m in moves)
