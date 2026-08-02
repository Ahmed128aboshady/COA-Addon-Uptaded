# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_locations = fields.Boolean('Restrict Location')

    stock_location_ids = fields.Many2many(
        'stock.location',
        'location_security_stock_location_users',
        'user_id',
        'location_id',
        'Stock Locations')

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_users_rel',
        'user_id', 'picking_type_id', string='Default Warehouse Operations')
    allowed_warehouse_ids = fields.Many2many(
        'stock.warehouse', string='Allowed Warehouses')


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.constrains('state', 'location_id', 'location_dest_id')
    def check_user_location_rights(self):
        # Skip the check entirely when running as superuser (sudo context).
        # This covers: button_validate, return wizard, and any other sudo flow.
        if self.env.su:
            return True

        for move in self:
            if move.state == 'draft':
                return True
            user_locations = self.env.user.stock_location_ids
            if self.env.user.restrict_locations:
                message = _(
                    'Invalid Location. You cannot process this move since you do '
                    'not control the location "%s". '
                    'Please contact your Adminstrator.')
                if move.location_id not in user_locations:
                    raise UserError(message % move.location_id.name)
                elif move.location_dest_id not in user_locations:
                    raise UserError(message % move.location_dest_id.name)


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        # Run the return creation as superuser so location access rules
        # on the newly created picking/moves don't block restricted users.
        return super(ReturnPicking, self.sudo())._create_returns()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    user_allowed_warehouse_ids = fields.Many2many(
        'stock.warehouse',
        compute='_compute_user_allowed_warehouses',
        string="User Allowed Warehouses",
        store=False,
    )

    @api.onchange('partner_id')
    def _compute_user_allowed_warehouses(self):
        for record in self:
            record.user_allowed_warehouse_ids = self.env.user.allowed_warehouse_ids


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    allowed_location_ids = fields.Many2many(
        'stock.location',
        compute='_compute_allowed_location_ids',
    )

    location_src_id = fields.Many2one(
        'stock.location',
        domain="[('id', 'in', allowed_location_ids)]",
    )

    @api.depends_context('uid')
    def _compute_allowed_location_ids(self):
        user = self.env.user
        base_domain = [
            '|',
            ('company_id', '=', False),
            ('company_id', 'in', self.env.companies.ids),
            ('usage', '=', 'internal'),
        ]
        if user.restrict_locations:
            base_domain = [
                ('id', 'in', user.stock_location_ids.ids)
            ] + base_domain

        locations = self.env['stock.location'].search(base_domain)
        for rec in self:
            rec.allowed_location_ids = locations


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    allowed_location_ids = fields.Many2many(
        'stock.location',
        compute='_compute_allowed_location_ids',
    )

    location_id = fields.Many2one(
        domain="[('id', 'in', allowed_location_ids)]",
    )

    location_dest_id = fields.Many2one(
        domain="[('id', 'in', allowed_location_ids)]",
    )

    @api.depends_context('uid')
    def _compute_allowed_location_ids(self):
        user = self.env.user
        base_domain = [
            '|',
            ('company_id', '=', False),
            ('company_id', 'in', self.env.companies.ids),
            ('usage', '=', 'internal'),
        ]
        if user.restrict_locations:
            base_domain = [
                ('id', 'in', user.stock_location_ids.ids)
            ] + base_domain

        locations = self.env['stock.location'].search(base_domain)
        for rec in self:
            rec.allowed_location_ids = locations

    def button_validate(self):
        return super(StockPicking, self.sudo()).button_validate()