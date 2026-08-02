# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class MfgMaintenance(models.Model):
    _name = 'mfg.maintenance'
    _description = 'Maintenance Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Maintenance Number', readonly=True, copy=False, default='New')
    machine_id = fields.Many2one('mfg.machine', string='Machine', required=True, tracking=True)
    maintenance_type = fields.Selection([
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
        ('emergency', 'Emergency'),
    ], string='Maintenance Type', required=True, default='preventive', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    date = fields.Date(string='Maintenance Date', required=True, default=fields.Date.today)
    date_done = fields.Date(string='Completion Date')
    technician_id = fields.Many2one('res.partner', string='Technician')
    description = fields.Text(string='Problem Description', required=True)
    solution = fields.Text(string='Solution')

    # Labor costs
    labor_hours = fields.Float(string='Labor Hours', digits=(16, 2))
    labor_rate = fields.Float(string='Hourly Rate', digits=(16, 2))
    labor_cost = fields.Float(string='Labor Cost', compute='_compute_costs', store=True)

    # Spare parts
    spare_parts_ids = fields.One2many('mfg.maintenance.part', 'maintenance_id', string='Spare Parts')
    spare_parts_cost = fields.Float(string='Spare Parts Cost', compute='_compute_costs', store=True)

    # Total
    total_cost = fields.Float(string='Total Cost', compute='_compute_costs', store=True)

    # Accounting
    journal_id = fields.Many2one('account.journal', string='Journal')
    move_id = fields.Many2one('account.move', string='Journal Entry', readonly=True)
    account_posted = fields.Boolean(string='Entry Posted', default=False)

    next_maintenance_date = fields.Date(string='Next Maintenance Date')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('mfg.maintenance') or 'New'
        return super().create(vals_list)

    @api.depends('labor_hours', 'labor_rate', 'spare_parts_ids.total_cost')
    def _compute_costs(self):
        for rec in self:
            rec.labor_cost = rec.labor_hours * rec.labor_rate
            rec.spare_parts_cost = sum(rec.spare_parts_ids.mapped('total_cost'))
            rec.total_cost = rec.labor_cost + rec.spare_parts_cost

    def action_start(self):
        self.state = 'in_progress'
        self.machine_id.state = 'maintenance'

    def action_done(self):
        self.state = 'done'
        self.date_done = date.today()
        self.machine_id.state = 'active'

    def action_cancel(self):
        self.state = 'cancelled'
        if self.machine_id.state == 'maintenance':
            self.machine_id.state = 'active'

    def _get_account(self, param_name):
        """Read account from settings"""
        param = self.env['ir.config_parameter'].sudo().get_param(param_name)
        if param:
            return self.env['account.account'].browse(int(param)).exists()
        return self.env['account.account']

    def action_post_accounting(self):
        """Create accounting entry for maintenance"""
        self.ensure_one()
        if self.account_posted:
            raise ValidationError('The accounting entry has already been posted!')
        if not self.total_cost:
            raise ValidationError('There are no costs to post!')

        machine = self.machine_id

        # Debit account: from settings or from machine
        debit_account = (
            self._get_account('manufacturing_machines.maintenance_cost_account_id')
            or machine.account_maintenance_id
        )
        if not debit_account:
            raise ValidationError(
                'Please set the maintenance cost account in Settings or on the machine!')

        # Credit account: from settings
        contra_account = self._get_account('manufacturing_machines.contra_account_id')
        if not contra_account:
            raise ValidationError('Please set the contra (credit) account in Settings!')

        # Journal
        param_j = self.env['ir.config_parameter'].sudo().get_param(
            'manufacturing_machines.machine_journal_id')
        journal = (
            self.journal_id
            or (self.env['account.journal'].browse(int(param_j)).exists() if param_j else False)
            or self.env['account.journal'].search([('type', '=', 'general')], limit=1)
        )
        if not journal:
            raise ValidationError('No accounting journal found!')

        move_vals = {
            'move_type': 'entry',
            'journal_id': journal.id,
            'date': self.date_done or self.date,
            'ref': f'Maintenance: {self.name} - {machine.name}',
            'line_ids': [
                (0, 0, {
                    'name': f'Maintenance cost - {machine.name}',
                    'account_id': debit_account.id,
                    'debit': self.total_cost,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': f'Maintenance payable - {machine.name}',
                    'account_id': contra_account.id,
                    'debit': 0.0,
                    'credit': self.total_cost,
                }),
            ],
        }
        move = self.env['account.move'].create(move_vals)
        move.action_post()
        self.move_id = move
        self.account_posted = True


class MfgMaintenancePart(models.Model):
    _name = 'mfg.maintenance.part'
    _description = 'Spare Part'

    maintenance_id = fields.Many2one('mfg.maintenance', string='Maintenance', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Spare Part')
    name = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, digits=(16, 2))
    unit_cost = fields.Float(string='Unit Price', digits=(16, 2))
    total_cost = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('quantity', 'unit_cost')
    def _compute_total(self):
        for rec in self:
            rec.total_cost = rec.quantity * rec.unit_cost

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.name = self.product_id.name
            self.unit_cost = self.product_id.standard_price
