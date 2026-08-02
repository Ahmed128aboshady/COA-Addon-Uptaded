from odoo import models, fields, api


class ManufacturingMachine(models.Model):
    _name = 'manufacturing.machine'
    _description = 'Manufacturing Machine'
    _order = 'name'

    name = fields.Char(string='Machine Name', required=True)
    code = fields.Char(string='Code')
    hourly_cost = fields.Float(string='Cost per Hour', digits=(16, 2), default=0.0)
    active = fields.Boolean(default=True)
    notes = fields.Text(string='Notes')


class MrpProductionMachineLine(models.Model):
    _name = 'mrp.production.machine.line'
    _description = 'Production Machine Line'
    _order = 'sequence, id'

    production_id = fields.Many2one(
        'mrp.production', string='Production Order',
        required=True, ondelete='cascade',
    )
    sequence = fields.Integer(default=10)
    machine_id = fields.Many2one(
        'manufacturing.machine', string='Machine', required=True,
    )
    machine_hourly_cost = fields.Float(
        string='Rate/hr', digits=(16, 2),
        related='machine_id.hourly_cost', store=True,
    )
    duration = fields.Float(string='Hours', digits=(16, 2), default=0.0)
    cost = fields.Float(
        string='Cost', digits=(16, 2),
        compute='_compute_cost', store=True,
    )
    state = fields.Selection([
        ('planned', 'Planned'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('stopped', 'Stopped'),
    ], string='Status', default='planned')

    @api.depends('machine_hourly_cost', 'duration')
    def _compute_cost(self):
        for rec in self:
            rec.cost = rec.machine_hourly_cost * rec.duration


class MrpProductionLaborLine(models.Model):
    _name = 'mrp.production.labor.line'
    _description = 'Production Labor Line'
    _order = 'sequence, id'

    production_id = fields.Many2one(
        'mrp.production', string='Production Order',
        required=True, ondelete='cascade',
    )
    sequence = fields.Integer(default=10)
    employee_name = fields.Char(string='Worker', required=True)
    job_title = fields.Char(string='Job Title')
    hourly_rate = fields.Float(string='Rate/hr', digits=(16, 2), default=0.0)
    hours = fields.Float(string='Hours', digits=(16, 2), default=0.0)
    total_cost = fields.Float(
        string='Total', digits=(16, 2),
        compute='_compute_total_cost', store=True,
    )

    @api.depends('hourly_rate', 'hours')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.hourly_rate * rec.hours


class MrpProductionOverheadLine(models.Model):
    _name = 'mrp.production.overhead.line'
    _description = 'Production Overhead Line'
    _order = 'sequence, id'

    production_id = fields.Many2one(
        'mrp.production', string='Production Order',
        required=True, ondelete='cascade',
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Item', required=True)
    overhead_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('variable', 'Variable'),
        ('other', 'Other'),
    ], string='Type', default='fixed')
    amount = fields.Float(string='Amount', digits=(16, 2), default=0.0)
