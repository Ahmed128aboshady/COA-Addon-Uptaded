# -*- coding: utf-8 -*-
from odoo import models, api


def _is_restriction_enabled(env):
    try:
        env.cr.execute(
            "SELECT location_restriction_enabled FROM res_users WHERE id = %s",
            (env.uid,)
        )
        row = env.cr.fetchone()
        return bool(row and row[0])
    except Exception:
        env.cr.rollback()
        return False


def _get_allowed_location_ids(env):
    env.cr.execute(
        "SELECT location_id FROM res_users_stock_location_rel WHERE user_id = %s",
        (env.uid,)
    )
    return [row[0] for row in env.cr.fetchall()]


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, *, active_test=True, bypass_access=False):
        if not self.env.su and active_test and _is_restriction_enabled(self.env):
            allowed_location_ids = _get_allowed_location_ids(self.env)
            if allowed_location_ids:
                all_allowed = self.env['stock.location'].sudo().search([
                    '|', ('usage', 'in', ['supplier', 'customer', 'inventory', 'production']),
                         ('id', 'child_of', allowed_location_ids),
                ])
                loc_ids = all_allowed.ids
                domain = ['|',
                    ('location_id', 'in', loc_ids),
                    ('location_dest_id', 'in', loc_ids),
                ] + list(domain or [])
        return super()._search(domain, offset=offset, limit=limit, order=order,
                               active_test=active_test, bypass_access=bypass_access)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, *, active_test=True, bypass_access=False):
        if not self.env.su and active_test and _is_restriction_enabled(self.env):
            allowed_location_ids = _get_allowed_location_ids(self.env)
            if allowed_location_ids:
                all_allowed = self.env['stock.location'].sudo().search([
                    '|', ('usage', 'in', ['supplier', 'customer', 'inventory', 'production']),
                         ('id', 'child_of', allowed_location_ids),
                ])
                loc_ids = all_allowed.ids
                domain = ['|',
                    ('location_id', 'in', loc_ids),
                    ('location_dest_id', 'in', loc_ids),
                ] + list(domain or [])
        return super()._search(domain, offset=offset, limit=limit, order=order,
                               active_test=active_test, bypass_access=bypass_access)
