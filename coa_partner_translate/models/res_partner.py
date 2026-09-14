# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(translate=True)
    company_name = fields.Char(translate=True)

    name_ar = fields.Char(
        string='Arabic Name / الاسم بالعربية',
        help='Name of the partner in Arabic',
    )
    name_en = fields.Char(
        string='English Name / الاسم بالإنجليزية',
        help='Name of the partner in English',
    )

    def _sync_name_translations(self):
        """Push name_ar / name_en into Odoo translation store."""
        for record in self:
            translations = {}
            if record.name_ar:
                translations['ar_001'] = record.name_ar
            if record.name_en:
                translations['en_US'] = record.name_en
            if translations:
                record._update_field_translations('name', translations)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_name_translations()
        return records

    def write(self, vals):
        result = super().write(vals)
        if 'name_ar' in vals or 'name_en' in vals:
            self._sync_name_translations()
        return result

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
