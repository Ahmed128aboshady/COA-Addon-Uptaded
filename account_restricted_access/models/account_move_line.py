# -*- coding: utf-8 -*-
from odoo import models
from odoo.fields import Domain


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _search(self, domain, offset=0, limit=None, order=None,
                *, active_test=True, bypass_access=False):
        """
        Restrict journal-item visibility for restricted accountants.
        Because accounting reports call account.move.line._search() internally
        via _get_report_query(), this override filters ALL reports (General
        Ledger, Trial Balance, Aged Receivable, …) automatically.
        Skipped in sudo mode so posting/reconciliation is never blocked.
        """
        if (
            not self.env.su
            and self.env.user.has_group(
                'account_restricted_access.group_account_restricted'
            )
        ):
            allowed_ids = self.env.user.sudo().allowed_account_ids.ids
            domain = Domain(domain) & Domain([('account_id', 'in', allowed_ids)])

        return super()._search(
            domain, offset=offset, limit=limit, order=order,
            active_test=active_test, bypass_access=bypass_access,
        )
