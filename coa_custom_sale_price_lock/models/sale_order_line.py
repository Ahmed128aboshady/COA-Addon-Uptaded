from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_price_editable = fields.Boolean(
        compute='_compute_is_price_editable',
        default=False
    )

    def _compute_is_price_editable(self):
        can_edit = self.env.user.has_group('custom_sale_price_lock.group_edit_sale_price')
        for line in self:
            is_service = line.product_id.type == 'service'
            line.is_price_editable = can_edit or is_service