# -*- coding: utf-8 -*-
from odoo import models, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    def _is_location_restriction_enabled(self):
        try:
            self.env.cr.execute(
                "SELECT location_restriction_enabled FROM res_users WHERE id = %s",
                (self.env.uid,)
            )
            row = self.env.cr.fetchone()
            return bool(row and row[0])
        except Exception:
            self.env.cr.rollback()
            return False

    def _get_user_allowed_warehouse_ids(self):
        self.env.cr.execute(
            "SELECT warehouse_id FROM res_users_stock_warehouse_rel WHERE user_id = %s",
            (self.env.uid,)
        )
        return [row[0] for row in self.env.cr.fetchall()]

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, *, active_test=True, bypass_access=False):
        if not self.env.su and active_test and self._is_location_restriction_enabled():
            allowed_ids = self._get_user_allowed_warehouse_ids()
            if allowed_ids:
                domain = [('id', 'in', allowed_ids)] + list(domain or [])
        return super()._search(domain, offset=offset, limit=limit, order=order, active_test=active_test, bypass_access=bypass_access)
