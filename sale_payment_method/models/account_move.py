from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_method_ids = fields.Many2many(
        comodel_name='sale.payment.method',
        relation='account_move_payment_method_rel',
        column1='move_id',
        column2='payment_method_id',
        string='Payment Methods',
        tracking=True,
    )

    @api.onchange('partner_id')
    def _onchange_partner_payment_method(self):
        """Auto-fill payment methods from the customer's defaults (only if not already set)."""
        if self.partner_id and self.partner_id.payment_method_ids and not self.payment_method_ids:
            self.payment_method_ids = self.partner_id.payment_method_ids
