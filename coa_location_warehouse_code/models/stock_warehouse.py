from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    warehouse_code = fields.Char(
        string='Code',
        size=10,
        help='Short unique code to identify this warehouse.',
    )
