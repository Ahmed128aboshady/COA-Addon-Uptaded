from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    secondary_uom_id = fields.Many2one(
        related='product_id.secondary_uom_id', string='Secondary UoM')
    has_secondary_uom = fields.Boolean(
        related='product_id.has_secondary_uom')
    secondary_quantity = fields.Float(
        'Secondary Quantity', digits='Product Unit', default=0.0,
        help="Quantity in the secondary unit of measure.")
