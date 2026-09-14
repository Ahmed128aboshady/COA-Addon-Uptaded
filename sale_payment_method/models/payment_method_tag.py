from odoo import fields, models


class SalePaymentMethod(models.Model):
    _name = 'sale.payment.method'
    _description = 'Payment Method'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color Index')
