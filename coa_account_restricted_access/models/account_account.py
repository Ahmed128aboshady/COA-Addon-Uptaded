# -*- coding: utf-8 -*-
from odoo import models
from odoo.fields import Domain


class AccountAccount(models.Model):
    _inherit = 'account.account'

    def _search(self, domain, offset=0, limit=None, order=None,
                *, active_test=True, bypass_access=False):
        """
        Restrict chart-of-accounts visibility for restricted accountants.
        Skipped in sudo mode so internal/system code is never blocked.
        """
        if (
            not self.env.su
            and self.env.user.has_group(
                'account_restricted_access.group_account_restricted'
            )
        ):
            allowed_ids = self.env.user.sudo().allowed_account_ids.ids
            domain = Domain(domain) & Domain([('id', 'in', allowed_ids)])

        return super()._search(
            domain, offset=offset, limit=limit, order=order,
            active_test=active_test, bypass_access=bypass_access,
        )
