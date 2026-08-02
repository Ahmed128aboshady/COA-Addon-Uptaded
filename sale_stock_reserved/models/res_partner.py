from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_unreserve_sale_stock(self):
        """Unreserve all reserved stock moves linked to sale orders for this customer."""
        moves = self.env['stock.move'].search([
            ('picking_id.sale_id.partner_id', 'in', self.ids),
            ('state', 'in', ('confirmed', 'waiting', 'partially_available', 'assigned')),
            ('picking_id.state', 'not in', ('done', 'cancel')),
            ('quantity', '>', 0),
        ])
        moves._do_unreserve()
        return {'type': 'ir.actions.client', 'tag': 'reload'}
