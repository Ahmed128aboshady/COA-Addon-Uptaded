from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # No default on purpose: the category drives the product code, so the
    # user must consciously pick it — a default would silently file new
    # products under the wrong category.
    categ_id = fields.Many2one(required=True)

    @api.model
    def name_create(self, name):
        # Quick create from a many2one popup sends only the name; without a
        # category no code can be generated, so guide the user to the full
        # form instead of failing on the required constraint.
        if not self.env.context.get('default_categ_id'):
            raise UserError(_(
                'A Product Category is required to generate the product code.\n'
                'Please use "Create and edit..." and select a category.'
            ))
        return super().name_create(name)

    # ── Sequence helpers ────────────────────────────────────────────────────

    def _categ_seq_code(self, categ_id):
        return f'product.categ.{categ_id}'

    def _get_or_create_categ_sequence(self, categ_id):
        """Return the ir.sequence code for categ_id, creating it if missing.

        Prefix rule: {N chars of category name}-
        Start with 1 char; keep adding chars until the prefix is unique
        among all existing category sequences.
        """
        seq_code = self._categ_seq_code(categ_id)
        IrSeq = self.env['ir.sequence'].sudo()

        if IrSeq.search([('code', '=', seq_code)], limit=1):
            return seq_code

        categ = self.env['product.category'].browse(categ_id)
        # Strip to alpha chars only for a clean prefix
        raw = ''.join(c for c in (categ.name or 'X').upper() if c.isalpha()) or 'X'

        existing_prefixes = set(
            IrSeq.search([('code', 'like', 'product.categ.%')]).mapped('prefix')
        )

        chosen = raw  # fallback: full name
        for n in range(1, len(raw) + 1):
            candidate = f'{raw[:n]}-'
            if candidate not in existing_prefixes:
                chosen = raw[:n]
                break

        IrSeq.create({
            'name': f'Product Code [{categ.complete_name}]',
            'code': seq_code,
            'prefix': f'{chosen}-',
            'padding': 7,
            'number_next': 1,
            'number_increment': 1,
            'company_id': False,
        })
        return seq_code

    def _next_code_for_categ(self, categ_id):
        seq_code = self._get_or_create_categ_sequence(categ_id)
        return self.env['ir.sequence'].next_by_code(seq_code) or 'New'

    # ── ORM overrides ────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        # When the creation is driven from product.product (quick create /
        # "Create and edit" popups, variant form, ...) the core sets
        # create_product_product=False in the context. In that flow the
        # variant is created empty AFTER the template, and default_code on
        # the template is recomputed from the variant — any code generated
        # here would be wiped. The product.product override handles it.
        variant_driven = self.env.context.get('create_product_product', True) is False
        if not variant_driven:
            for vals in vals_list:
                if not vals.get('default_code'):
                    # quick create / programmatic create may not pass categ_id:
                    # fall back to the default category the record will get
                    categ_id = vals.get('categ_id') or self.default_get(['categ_id']).get('categ_id')
                    if categ_id:
                        vals['default_code'] = self._next_code_for_categ(categ_id)
        templates = super().create(vals_list)
        # Propagate the code to the single variant when the inverse hasn't run yet
        for template in templates:
            if template.default_code and len(template.product_variant_ids) == 1:
                variant = template.product_variant_ids
                if not variant.default_code:
                    variant.default_code = template.default_code
        return templates

    def copy(self, default=None):
        default = dict(default or {})
        if 'default_code' not in default:
            categ_id = default.get('categ_id') or self.categ_id.id
            if categ_id:
                default['default_code'] = self._next_code_for_categ(categ_id)
        return super().copy(default)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_create(self, name):
        if not self.env.context.get('default_categ_id'):
            raise UserError(_(
                'A Product Category is required to generate the product code.\n'
                'Please use "Create and edit..." and select a category.'
            ))
        return super().name_create(name)

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product, vals in zip(products, vals_list):
            if vals.get('default_code') or vals.get('product_tmpl_id'):
                # variants attached to an existing template (e.g. generated
                # by _create_variant_ids) are handled at template level
                continue
            if not product.default_code and product.categ_id:
                product.default_code = product.product_tmpl_id._next_code_for_categ(
                    product.categ_id.id
                )
        return products
