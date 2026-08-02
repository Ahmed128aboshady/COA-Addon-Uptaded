from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_color = fields.Char(string='Color')
