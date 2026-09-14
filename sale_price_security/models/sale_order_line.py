from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_edit_readonly = fields.Boolean(
        compute='_compute_price_edit_readonly',
    )

    @api.depends_context('uid')
    def _compute_price_edit_readonly(self):
        """True when the current user does NOT have the price-edit permission."""
        can_edit = self.env.user.has_group(
            'sale_price_security.group_sale_price_edit'
        )
        for line in self:
            line.price_edit_readonly = not can_edit
