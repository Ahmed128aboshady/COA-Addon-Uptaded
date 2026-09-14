from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    requires_expiry_on_purchase = fields.Boolean(
        string='Requires Expiry Date on Purchase',
        default=False,
        help='If enabled, the receipt cannot be validated unless every '
             'move line for this product has an Expiry Date filled in. '
             'Also enforces Lot tracking automatically.',
    )

    @api.onchange('requires_expiry_on_purchase')
    def _onchange_requires_expiry_on_purchase(self):
        if self.requires_expiry_on_purchase:
            # Force lot tracking when expiry is required
            if self.tracking == 'none':
                self.tracking = 'lot'

    def write(self, vals):
        res = super().write(vals)
        if vals.get('requires_expiry_on_purchase'):
            # Ensure lot tracking is enabled
            self.filtered(lambda t: t.tracking == 'none').sudo().write({'tracking': 'lot'})
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    requires_expiry_on_purchase = fields.Boolean(
        related='product_tmpl_id.requires_expiry_on_purchase',
        store=True,
    )
