from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    payment_method_ids = fields.Many2many(
        comodel_name='sale.payment.method',
        relation='res_partner_sale_payment_method_rel',
        column1='partner_id',
        column2='payment_method_id',
        string='Payment Methods',
        help='Default payment methods used automatically on sales orders and invoices.',
    )
