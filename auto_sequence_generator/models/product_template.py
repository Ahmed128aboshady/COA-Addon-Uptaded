from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    categ_id = fields.Many2one(required=True)

    # ── Sequence helpers ────────────────────────────────────────────────────

    def _categ_seq_code(self, categ_id):
        return f'product.categ.{categ_id}'

    def _get_or_create_categ_sequence(self, categ_id):
        """Return the ir.sequence code for categ_id, creating it if missing.

        Prefix rule: PRD-{N chars of category name}-
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
            candidate = f'PRD-{raw[:n]}-'
            if candidate not in existing_prefixes:
                chosen = raw[:n]
                break

        IrSeq.create({
            'name': f'Product Code [{categ.complete_name}]',
            'code': seq_code,
            'prefix': f'PRD-{chosen}-',
            'padding': 7,
            'number_next': 1,
            'number_increment': 1,
            'company_id': False,
        })
        return seq_code

    # ── ORM overrides ────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('default_code') and vals.get('categ_id'):
                seq_code = self._get_or_create_categ_sequence(vals['categ_id'])
                vals['default_code'] = (
                    self.env['ir.sequence'].next_by_code(seq_code) or 'New'
                )
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
                seq_code = self._get_or_create_categ_sequence(categ_id)
                default['default_code'] = (
                    self.env['ir.sequence'].next_by_code(seq_code) or 'New'
                )
        return super().copy(default)
