# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ManufacturingMachine(models.Model):
    _name = 'mfg.machine'
    _description = 'Machine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Machine Name', required=True, tracking=True)
    code = fields.Char(string='Machine Code', readonly=True, copy=False, default='New')
    machine_type = fields.Selection([
        ('cutting', 'Cutting'),
        ('welding', 'Welding'),
        ('pressing', 'Pressing'),
        ('painting', 'Painting'),
        ('assembly', 'Assembly'),
        ('cnc', 'CNC'),
        ('lathe', 'Lathe'),
        ('other', 'Other'),
    ], string='Machine Type', required=True, tracking=True)
    state = fields.Selection([
        ('active', 'Running'),
        ('maintenance', 'Maintenance'),
        ('idle', 'Idle'),
        ('scrapped', 'Scrapped'),
    ], string='Status', default='active', tracking=True)

    # Purchase Data
    purchase_date = fields.Date(string='Purchase Date')
    purchase_cost = fields.Float(string='Purchase Cost', digits=(16, 2))
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    serial_number = fields.Char(string='Serial Number')
    warranty_expiry = fields.Date(string='Warranty Expiry')

    # Operating Costs
    hourly_cost = fields.Float(string='Hourly Cost', digits=(16, 2), default=0.0)
    depreciation_monthly = fields.Float(string='Monthly Depreciation', digits=(16, 2), default=0.0)

    # Accounts
    account_depreciation_id = fields.Many2one(
        'account.account', string='Depreciation Account',
        domain=[('account_type', 'in', ['expense'])])
    account_maintenance_id = fields.Many2one(
        'account.account', string='Maintenance Account',
        domain=[('account_type', 'in', ['expense'])])

    # Relations
    maintenance_ids = fields.One2many('mfg.maintenance', 'machine_id', string='Maintenance Records')
    production_ids = fields.One2many('mfg.production.order', 'machine_id', string='Production Orders')
    # Machine lines in official manufacturing orders (mrp.production)
    mrp_line_ids = fields.One2many('mfg.production.machine.line', 'machine_id', string='Usage in Manufacturing')

    # Statistics
    maintenance_count = fields.Integer(compute='_compute_counts', string='Maintenance Count')
    production_count = fields.Integer(compute='_compute_counts', string='Production Orders Count')
    total_maintenance_cost = fields.Float(compute='_compute_total_costs', string='Total Maintenance Cost')
    total_production_hours = fields.Float(compute='_compute_total_costs', string='Total Production Hours')

    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Machine Image')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('mfg.machine') or 'New'
        return super().create(vals_list)

    def _compute_counts(self):
        for rec in self:
            rec.maintenance_count = len(rec.maintenance_ids)
            # Official manufacturing orders (mrp.production) where this machine was used
            mrp_orders = rec.mrp_line_ids.mapped('production_id')
            rec.production_count = len(mrp_orders)

    def _compute_total_costs(self):
        for rec in self:
            rec.total_maintenance_cost = sum(rec.maintenance_ids.mapped('total_cost'))
            rec.total_production_hours = sum(rec.mrp_line_ids.mapped('duration'))

    def action_set_maintenance(self):
        self.state = 'maintenance'

    def action_set_active(self):
        self.state = 'active'

    def action_set_idle(self):
        self.state = 'idle'

    def action_view_maintenance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f'Maintenance {self.name}',
            'res_model': 'mfg.maintenance',
            'view_mode': 'list,form',
            'domain': [('machine_id', '=', self.id)],
            'context': {'default_machine_id': self.id},
        }

    def action_view_productions(self):
        # Open manufacturing orders (mrp.production) where this machine was used
        return {
            'type': 'ir.actions.act_window',
            'name': f'Production Orders — {self.name}',
            'res_model': 'mrp.production',
            'view_mode': 'list,form',
            'domain': [('machine_line_ids.machine_id', '=', self.id)],
        }
