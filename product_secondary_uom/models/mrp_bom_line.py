from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    secondary_uom_id = fields.Many2one(
        related='product_id.secondary_uom_id', string='Secondary UoM')
    has_secondary_uom = fields.Boolean(
        related='product_id.has_secondary_uom')
    secondary_product_qty = fields.Float(
        'Secondary Qty', digits='Product Unit', default=0.0,
        help="Quantity in the secondary unit of measure.")
