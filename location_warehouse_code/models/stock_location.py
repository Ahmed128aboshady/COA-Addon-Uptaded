from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    location_code = fields.Char(
        string='Code',
        size=10,
        help='Short unique code to identify this location.',
    )
