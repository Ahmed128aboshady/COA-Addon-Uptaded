from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_unreserve_sale_stock(self):
        """Unreserve all reserved stock moves linked to sale orders for this product."""
        moves = self.env['stock.move'].search([
            ('product_id', 'in', self.ids),
            ('picking_id.sale_id', '!=', False),
            ('state', 'in', ('confirmed', 'waiting', 'partially_available', 'assigned')),
            ('picking_id.state', 'not in', ('done', 'cancel')),
            ('quantity', '>', 0),
        ])
        moves._do_unreserve()
        return {'type': 'ir.actions.client', 'tag': 'reload'}
