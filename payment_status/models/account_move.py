from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        result = super().write(vals)
        if 'payment_state' in vals:
            self._update_picking_payment_status()
        return result

    def _update_picking_payment_status(self):
        """Trigger recomputation of payment_status on related stock pickings."""
        # From customer invoices → sale orders → pickings
        sale_orders = self.mapped('line_ids.sale_line_ids.order_id')
        pickings = sale_orders.mapped('picking_ids')

        # From vendor bills → purchase orders → pickings
        purchase_orders = self.mapped('line_ids.purchase_line_id.order_id')
        pickings |= purchase_orders.mapped('picking_ids')

        if pickings:
            self.env.add_to_compute(
                self.env['stock.picking']._fields['payment_status'],
                pickings,
            )
