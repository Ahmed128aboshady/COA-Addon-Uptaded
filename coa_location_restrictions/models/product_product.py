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


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, *, active_test=True, bypass_access=False):
        if not self.env.su and active_test and _is_restriction_enabled(self.env):
            allowed_location_ids = _get_allowed_location_ids(self.env)
            if allowed_location_ids:
                all_children = self.env['stock.location'].sudo().search([
                    ('id', 'child_of', allowed_location_ids),
                    ('usage', '=', 'internal'),
                ])
                loc_ids = all_children.ids
                if loc_ids:
                    self.env.cr.execute(
                        "SELECT DISTINCT product_id FROM stock_quant WHERE location_id = ANY(%s) AND quantity > 0",
                        (loc_ids,)
                    )
                    product_ids = [row[0] for row in self.env.cr.fetchall()]
                    domain = [('id', 'in', product_ids)] + list(domain or [])
        return super()._search(domain, offset=offset, limit=limit, order=order, active_test=active_test, bypass_access=bypass_access)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, *, active_test=True, bypass_access=False):
        if not self.env.su and active_test and _is_restriction_enabled(self.env):
            allowed_location_ids = _get_allowed_location_ids(self.env)
            if allowed_location_ids:
                all_children = self.env['stock.location'].sudo().search([
                    ('id', 'child_of', allowed_location_ids),
                    ('usage', '=', 'internal'),
                ])
                loc_ids = all_children.ids
                if loc_ids:
                    self.env.cr.execute(
                        """
                        SELECT DISTINCT pt.id
                        FROM product_template pt
                        JOIN product_product pp ON pp.product_tmpl_id = pt.id
                        JOIN stock_quant sq ON sq.product_id = pp.id
                        WHERE sq.location_id = ANY(%s) AND sq.quantity > 0
                        """,
                        (loc_ids,)
                    )
                    tmpl_ids = [row[0] for row in self.env.cr.fetchall()]
                    domain = [('id', 'in', tmpl_ids)] + list(domain or [])
        return super()._search(domain, offset=offset, limit=limit, order=order, active_test=active_test, bypass_access=bypass_access)
