from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    secondary_uom_id = fields.Many2one(
        'uom.uom', string='Secondary UoM', tracking=True,
        help="Independent secondary unit of measure for this product. "
             "No conversion is applied between primary and secondary UoM.")
    has_secondary_uom = fields.Boolean(
        string='Has Secondary UoM',
        compute='_compute_has_secondary_uom', store=True)

    @api.depends('secondary_uom_id')
    def _compute_has_secondary_uom(self):
        for template in self:
            template.has_secondary_uom = bool(template.secondary_uom_id)
