# -*- coding: utf-8 -*-
from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _search_display_name(self, operator, value):
        """Odoo 18 uses _search_display_name (not _name_search) to search
        partners across complete_name / email / ref / vat via _rec_names_search.
        The default 'ilike' logic matches *any* ref that contains the typed
        number, so searching '538' also returns '1538'.

        Override: when the user types a pure number, try an EXACT match on
        the Reference field first. If found, restrict results to those partners
        only. Otherwise fall back to the standard behaviour.
        """
        if (
            value
            and str(value).strip().isdigit()
            and operator in ('ilike', 'like', '=', '=ilike', '=like')
        ):
            exact = self.search([('ref', '=', str(value).strip())])
            if exact:
                return [('id', 'in', exact.ids)]

        return super()._search_display_name(operator, value)
