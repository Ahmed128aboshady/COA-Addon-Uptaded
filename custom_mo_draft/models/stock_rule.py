from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _should_auto_confirm_procurement_mo(self, mo):
        # If MO is created from a sale order, keep it in draft
        if mo.sale_line_id:
            return False
        return super()._should_auto_confirm_procurement_mo(mo)
