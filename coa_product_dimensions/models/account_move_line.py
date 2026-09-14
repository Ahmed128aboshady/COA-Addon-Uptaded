from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_amount = fields.Float(string='Discount Amount', digits='Product Price')

    @api.onchange('discount_amount', 'price_unit', 'quantity')
    def _onchange_discount_amount(self):
        """
        When the user enters a fixed discount amount, calculate the equivalent percentage
        and update the standard 'discount' field so Odoo handles the rest of the math.
        """
        for line in self:
            if line.discount_amount and line.price_unit and line.quantity:
                total_price = line.price_unit * line.quantity
                if total_price > 0:
                    # Calculate percentage: (Discount Amount / Total Price) * 100
                    line.discount = (line.discount_amount / total_price) * 100
            elif not line.discount_amount:
                line.discount = 0.0

    @api.onchange('discount', 'price_unit', 'quantity')
    def _onchange_discount_percentage(self):
        """
        If the user changes the percentage instead, update the fixed amount field to match.
        """
        for line in self:
            if line.discount and line.price_unit and line.quantity:
                total_price = line.price_unit * line.quantity
                line.discount_amount = total_price * (line.discount / 100.0)
            elif not line.discount:
                line.discount_amount = 0.0