# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    # ── enable restriction flag ───────────────────────────────────────────────
    location_restriction_enabled = fields.Boolean(
        string='Enable Location Restriction',
        help='When enabled, this user can only access the warehouses, '
             'locations and operation types listed below.',
    )

    # ── allowed warehouses ────────────────────────────────────────────────────
    allowed_warehouse_ids = fields.Many2many(
        comodel_name='stock.warehouse',
        relation='res_users_stock_warehouse_rel',
        column1='user_id',
        column2='warehouse_id',
        string='Allowed Warehouses',
    )

    # ── allowed locations ─────────────────────────────────────────────────────
    allowed_location_ids = fields.Many2many(
        comodel_name='stock.location',
        relation='res_users_stock_location_rel',
        column1='user_id',
        column2='location_id',
        string='Allowed Locations',
        domain="[('usage', 'in', ['internal', 'transit'])]",
    )

    # ── allowed operation types ───────────────────────────────────────────────
    allowed_picking_type_ids = fields.Many2many(
        comodel_name='stock.picking.type',
        relation='res_users_stock_picking_type_rel',
        column1='user_id',
        column2='picking_type_id',
        string='Allowed Operation Types',
    )

    # ── helpers ───────────────────────────────────────────────────────────────
    def _is_location_allowed(self, location):
        """Return True if location (or any parent) is in the allowed list."""
        self.ensure_one()
        if not self.location_restriction_enabled:
            return True
        if not self.allowed_location_ids:
            return True
        loc = location
        while loc:
            if loc in self.allowed_location_ids:
                return True
            loc = loc.location_id
        return False

    def _is_picking_type_allowed(self, picking_type):
        self.ensure_one()
        if not self.location_restriction_enabled:
            return True
        if not self.allowed_picking_type_ids:
            return True
        return picking_type in self.allowed_picking_type_ids

    def _is_warehouse_allowed(self, warehouse):
        self.ensure_one()
        if not self.location_restriction_enabled:
            return True
        if not self.allowed_warehouse_ids:
            return True
        return warehouse in self.allowed_warehouse_ids
