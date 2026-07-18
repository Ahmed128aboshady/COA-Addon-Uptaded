from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(readonly=True, copy=False)

    def _get_sequence_code(self, vals=None):
        ctx = self.env.context
        v = vals or {}
        is_vendor = (
            v.get('supplier_rank', 0)
            or ctx.get('default_supplier_rank', 0)
            or ctx.get('res_partner_search_mode') == 'supplier'
        )
        is_customer = (
            v.get('customer_rank', 0)
            or ctx.get('default_customer_rank', 0)
            or ctx.get('res_partner_search_mode') == 'customer'
        )
        if is_vendor:
            return 'res.partner.vendor'
        if is_customer:
            return 'res.partner.customer'
        return 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref'):
                seq_code = self._get_sequence_code(vals)
                vals['ref'] = self.env['ir.sequence'].next_by_code(seq_code) or 'New'
        return super().create(vals_list)

    def copy(self, default=None):
        default = dict(default or {})
        if 'ref' not in default:
            seq_code = self._get_sequence_code({
                'customer_rank': self.customer_rank,
                'supplier_rank': self.supplier_rank,
            })
            default['ref'] = self.env['ir.sequence'].next_by_code(seq_code) or 'New'
        return super().copy(default)
