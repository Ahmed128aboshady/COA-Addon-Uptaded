# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name_ar = fields.Char(
        string='Arabic Name / الاسم بالعربية',
        help='Name of the partner in Arabic',
    )
    name_en = fields.Char(
        string='English Name / الاسم بالإنجليزية',
        help='Name of the partner in English',
    )

    def _get_complete_name(self):
        res = super()._get_complete_name()
        if isinstance(res, dict):
            return (res.get('en_US') or next(iter(res.values()), '') if res else '').strip()
        return str(res or '').strip()

    def _compute_display_name(self):
        """Return Arabic name when UI language is Arabic, English name otherwise."""
        lang = self.env.context.get('lang', 'en_US')
        for partner in self:
            if lang == 'ar_001' and partner.name_ar:
                partner.display_name = partner.name_ar
            elif lang != 'ar_001' and partner.name_en:
                partner.display_name = partner.name_en
            else:
                super(ResPartner, partner)._compute_display_name()

