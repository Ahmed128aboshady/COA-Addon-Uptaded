# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MfgProductionOrder(models.Model):
    _name = 'mfg.production.order'
    _description = 'Production Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(string='Order Number', readonly=True, copy=False, default='New')
    machine_id = fields.Many2one('mfg.machine', string='Primary Machine', tracking=True)
    product_name = fields.Char(string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, digits=(16, 2))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    date_start = fields.Datetime(string='Start Date', tracking=True)
    date_end = fields.Datetime(string='End Date', tracking=True)
    planned_hours = fields.Float(string='Planned Hours', digits=(16, 2))

    # Machines with time tracking
    machine_line_ids = fields.One2many(
        'mfg.production.machine.line', 'mfg_order_id', string='Machines',
    )
    actual_hours = fields.Float(
        string='Actual Hours (Total)',
        compute='_compute_totals', store=True, digits=(16, 2),
    )
    machine_cost = fields.Float(compute='_compute_totals', store=True, string='Machine Cost')

    # Labor costs
    labor_lines = fields.One2many('mfg.labor.line', 'production_id', string='Workers')
    total_labor_cost = fields.Float(compute='_compute_totals', store=True, string='Labor Cost')

    # Overhead costs
    overhead_lines = fields.One2many('mfg.overhead.line', 'production_id', string='Overhead Costs')
    total_overhead = fields.Float(compute='_compute_totals', store=True, string='Total Overhead Costs')

    # Total
    total_cost = fields.Float(compute='_compute_totals', store=True, string='Total Cost')
    cost_per_unit = fields.Float(compute='_compute_totals', store=True, string='Unit Cost')

    # Accounting
    journal_id = fields.Many2one('account.journal', string='Journal')
    move_id = fields.Many2one('account.move', string='Journal Entry', readonly=True)
    account_posted = fields.Boolean(string='Entry Posted', default=False)

    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('mfg.production') or 'New'
        return super().create(vals_list)

    @api.depends(
        'labor_lines.total_cost',
        'overhead_lines.amount',
        'machine_line_ids.cost',
        'machine_line_ids.duration',
        'quantity',
    )
    def _compute_totals(self):
        for rec in self:
            rec.actual_hours = sum(rec.machine_line_ids.mapped('duration'))
            rec.total_labor_cost = sum(rec.labor_lines.mapped('total_cost'))
            rec.machine_cost = sum(rec.machine_line_ids.mapped('cost'))
            rec.total_overhead = sum(rec.overhead_lines.mapped('amount'))
            rec.total_cost = rec.total_labor_cost + rec.machine_cost + rec.total_overhead
            rec.cost_per_unit = rec.total_cost / rec.quantity if rec.quantity else 0.0

    def action_confirm(self):
        self.state = 'confirmed'

    def action_start(self):
        self.state = 'in_progress'
        if not self.date_start:
            self.date_start = fields.Datetime.now()

    def action_done(self):
        self.state = 'done'
        if not self.date_end:
            self.date_end = fields.Datetime.now()

    def action_cancel(self):
        self.state = 'cancelled'

    def _get_account(self, param_name):
        """Read account from settings"""
        param = self.env['ir.config_parameter'].sudo().get_param(param_name)
        if param:
            return self.env['account.account'].browse(int(param)).exists()
        return self.env['account.account']

    def _get_journal(self):
        """Read journal from settings"""
        param = self.env['ir.config_parameter'].sudo().get_param(
            'manufacturing_machines.machine_journal_id')
        if param:
            journal = self.env['account.journal'].browse(int(param)).exists()
            if journal:
                return journal
        return self.env['account.journal'].search([('type', '=', 'general')], limit=1)

    def action_post_accounting(self):
        """Create accounting entry for production order"""
        self.ensure_one()
        if self.account_posted:
            raise ValidationError('The accounting entry has already been posted!')
        if not self.total_cost:
            raise ValidationError('There are no costs to post!')

        journal = self.journal_id or self._get_journal()
        if not journal:
            raise ValidationError('No journal found — please set one in Settings!')

        labor_account = self._get_account('manufacturing_machines.labor_cost_account_id')
        machine_account = self._get_account('manufacturing_machines.machine_cost_account_id')
        overhead_account = self._get_account('manufacturing_machines.overhead_cost_account_id')
        contra_account = self._get_account('manufacturing_machines.contra_account_id')

        if not contra_account:
            raise ValidationError('Please set the contra (credit) account in Settings!')

        lines = []
        if self.total_labor_cost and labor_account:
            lines.append((0, 0, {
                'name': f'Labor cost - {self.name}',
                'account_id': labor_account.id,
                'debit': self.total_labor_cost,
                'credit': 0.0,
            }))
        if self.machine_cost and machine_account:
            lines.append((0, 0, {
                'name': f'Machine cost - {self.name}',
                'account_id': machine_account.id,
                'debit': self.machine_cost,
                'credit': 0.0,
            }))
        if self.total_overhead and overhead_account:
            lines.append((0, 0, {
                'name': f'Overhead costs - {self.name}',
                'account_id': overhead_account.id,
                'debit': self.total_overhead,
                'credit': 0.0,
            }))

        if not lines:
            raise ValidationError('Please set the cost accounts in Settings first!')

        lines.append((0, 0, {
            'name': f'Total production cost - {self.name}',
            'account_id': contra_account.id,
            'debit': 0.0,
            'credit': sum(l[2]['debit'] for l in lines),
        }))

        move = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': journal.id,
            'date': fields.Date.today(),
            'ref': f'Production Order: {self.name} - {self.product_name}',
            'line_ids': lines,
        })
        move.action_post()
        self.move_id = move
        self.account_posted = True


class MfgLaborLine(models.Model):
    _name = 'mfg.labor.line'
    _description = 'Worker Line'

    production_id = fields.Many2one('mfg.production.order', string='Production Order', ondelete='cascade')
    employee_name = fields.Char(string='Worker Name', required=True)
    job_title = fields.Char(string='Job Title')
    hours = fields.Float(string='Work Hours', digits=(16, 2))
    hourly_rate = fields.Float(string='Hourly Rate', digits=(16, 2))
    total_cost = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('hours', 'hourly_rate')
    def _compute_total(self):
        for rec in self:
            rec.total_cost = rec.hours * rec.hourly_rate


class MfgOverheadLine(models.Model):
    _name = 'mfg.overhead.line'
    _description = 'Overhead Cost'

    production_id = fields.Many2one('mfg.production.order', string='Production Order', ondelete='cascade')
    name = fields.Char(string='Item', required=True)
    overhead_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('rent', 'Rent'),
        ('water', 'Water'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ], string='Type', default='other')
    amount = fields.Float(string='Amount', digits=(16, 2))
