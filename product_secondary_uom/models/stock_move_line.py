from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    secondary_quantity = fields.Float(
        'Secondary Quantity', digits='Product Unit', default=0.0,
        help="Done quantity in the secondary unit of measure.")
    secondary_uom_id = fields.Many2one(
        related='move_id.secondary_uom_id', string='Secondary UoM')
    has_secondary_uom = fields.Boolean(
        related='move_id.has_secondary_uom')
