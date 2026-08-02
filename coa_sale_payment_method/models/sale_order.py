from odoo import Command, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_method_ids = fields.Many2many(
        comodel_name='sale.payment.method',
        relation='sale_order_payment_method_rel',
        column1='order_id',
        column2='payment_method_id',
        string='Payment Methods',
        tracking=True,
    )

    @api.onchange('partner_id')
    def _onchange_partner_payment_method(self):
        """Auto-fill payment methods from the customer's defaults."""
        if self.partner_id and self.partner_id.payment_method_ids:
            self.payment_method_ids = self.partner_id.payment_method_ids

    def _prepare_invoice(self):
        """Pass payment_methods to the generated invoice."""
        vals = super()._prepare_invoice()
        if self.payment_method_ids:
            vals['payment_method_ids'] = [Command.set(self.payment_method_ids.ids)]
        return vals
