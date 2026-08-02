from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super()._get_custom_move_fields()
        fields += ['secondary_product_uom_qty', 'secondary_uom_id']
        return fields
