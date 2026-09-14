from odoo import api, fields, models, _

class SaleOrder(models.Model):
    """ inherit sale Order """

    _inherit = 'sale.order'