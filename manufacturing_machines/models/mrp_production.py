# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class MfgMrpLaborLine(models.Model):
    """Worker cost line linked to an MRP manufacturing order"""
    _name = 'mfg.mrp.labor.line'
    _description = 'Labor Line in MRP Production'

    mrp_production_id = fields.Many2one(
        'mrp.production', string='Manufacturing Order',
        ondelete='cascade', index=True,
    )
    employee_name = fields.Char(string='Worker Name', required=True)
    job_title = fields.Char(string='Job Title')
    hours = fields.Float(string='Work Hours', digits=(16, 2))
    hourly_rate = fields.Float(string='Hourly Rate', digits=(16, 2))
    total_cost = fields.Float(
        string='Total', compute='_compute_total', store=True,
    )

    @api.depends('hours', 'hourly_rate')
    def _compute_total(self):
        for rec in self:
            rec.total_cost = rec.hours * rec.hourly_rate


class MfgMrpOverheadLine(models.Model):
    """Overhead cost line linked to an MRP manufacturing order"""
    _name = 'mfg.mrp.overhead.line'
    _description = 'Overhead Cost in MRP Production'

    mrp_production_id = fields.Many2one(
        'mrp.production', string='Manufacturing Order',
        ondelete='cascade', index=True,
    )
    name = fields.Char(string='Item', required=True)
    overhead_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('rent', 'Rent'),
        ('water', 'Water'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ], string='Type', default='other')
    amount = fields.Float(string='Amount', digits=(16, 2))


class MfgProductionMachineLine(models.Model):
    """Machine line in manufacturing order — works like a Work Order but simpler"""
    _name = 'mfg.production.machine.line'
    _description = 'Machine Usage in Production'
    _order = 'sequence, id'

    production_id = fields.Many2one(
        'mrp.production', string='Manufacturing Order (MRP)',
        ondelete='cascade', index=True,
    )
    mfg_order_id = fields.Many2one(
        'mfg.production.order', string='Production Order',
        ondelete='cascade', index=True,
    )
    sequence = fields.Integer(default=10)
    machine_id = fields.Many2one(
        'mfg.machine', string='Machine', required=True,
    )
    machine_hourly_cost = fields.Float(
        string='Hourly Cost',
        related='machine_id.hourly_cost', readonly=True,
    )
    state = fields.Selection([
        ('draft',   'Pending'),
        ('running', 'Running'),
        ('paused',  'Paused'),
        ('done',    'Done'),
    ], string='Status', default='draft', required=True)

    # Timing
    date_start = fields.Datetime(string='Start Time')
    date_end   = fields.Datetime(string='End Time')
    duration   = fields.Float(
        string='Duration (Hours)', digits=(16, 2),
        compute='_compute_duration', store=True,
    )
    cost = fields.Float(
        string='Cost', digits=(16, 2),
        compute='_compute_duration', store=True,
    )

    @api.depends('date_start', 'date_end', 'machine_id.hourly_cost')
    def _compute_duration(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                delta = rec.date_end - rec.date_start
                rec.duration = delta.total_seconds() / 3600
            elif rec.date_start:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc).replace(tzinfo=None)
                delta = now - rec.date_start
                rec.duration = delta.total_seconds() / 3600
            else:
                rec.duration = 0.0
            rec.cost = rec.duration * (rec.machine_id.hourly_cost or 0.0)

    def button_start(self):
        self.ensure_one()
        if self.state == 'running':
            raise UserError('The machine is already running.')
        self.write({
            'state': 'running',
            'date_start': fields.Datetime.now(),
        })
        self.machine_id.write({'state': 'active'})

    def button_pause(self):
        self.ensure_one()
        if self.state != 'running':
            raise UserError('The machine is not running.')
        self.write({'state': 'paused'})
        self.machine_id.write({'state': 'idle'})
        self._compute_duration()

    def button_resume(self):
        self.ensure_one()
        if self.state != 'paused':
            raise UserError('The machine is not in a paused state.')
        self.write({'state': 'running'})
        self.machine_id.write({'state': 'active'})

    def button_done(self):
        self.ensure_one()
        self.write({
            'state': 'done',
            'date_end': fields.Datetime.now(),
        })
        self.machine_id.write({'state': 'idle'})
        self._compute_duration()


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # ── Machines ──────────────────────────────────────────────────────────────
    machine_line_ids = fields.One2many(
        'mfg.production.machine.line', 'production_id',
        string='Machines',
    )
    primary_machine_id = fields.Many2one(
        'mfg.machine', string='Machine',
        compute='_compute_primary_machine', store=True,
        help='First machine in the machines list — used for grouping and filtering',
    )
    machine_total_hours = fields.Float(
        string='Total Machine Hours',
        compute='_compute_machine_totals', store=True,
        digits=(16, 2),
    )
    machine_total_cost = fields.Float(
        string='Total Machine Cost',
        compute='_compute_machine_totals', store=True,
        digits=(16, 2),
    )

    # ── Labor ─────────────────────────────────────────────────────────────────
    labor_line_ids = fields.One2many(
        'mfg.mrp.labor.line', 'mrp_production_id',
        string='Workers',
    )
    mrp_labor_cost = fields.Float(
        string='Labor Cost',
        compute='_compute_mrp_costs', store=True,
        digits=(16, 2),
    )

    # ── Overhead ──────────────────────────────────────────────────────────────
    overhead_line_ids = fields.One2many(
        'mfg.mrp.overhead.line', 'mrp_production_id',
        string='Overhead Costs',
    )
    mrp_overhead_cost = fields.Float(
        string='Overhead Cost',
        compute='_compute_mrp_costs', store=True,
        digits=(16, 2),
    )

    # ── Grand Total ───────────────────────────────────────────────────────────
    mrp_grand_total = fields.Float(
        string='Grand Total Cost',
        compute='_compute_mrp_costs', store=True,
        digits=(16, 2),
    )

    # ── Accounting ────────────────────────────────────────────────────────────
    mrp_cost_posted = fields.Boolean(string='Entry Posted', default=False)
    mrp_move_id = fields.Many2one(
        'account.move', string='Journal Entry', readonly=True,
    )

    # ── Computes ──────────────────────────────────────────────────────────────
    @api.depends('machine_line_ids.machine_id')
    def _compute_primary_machine(self):
        for rec in self:
            first = rec.machine_line_ids[:1]
            rec.primary_machine_id = first.machine_id if first else False

    @api.depends('machine_line_ids.duration', 'machine_line_ids.cost')
    def _compute_machine_totals(self):
        for rec in self:
            rec.machine_total_hours = sum(rec.machine_line_ids.mapped('duration'))
            rec.machine_total_cost  = sum(rec.machine_line_ids.mapped('cost'))

    @api.depends(
        'labor_line_ids.total_cost',
        'overhead_line_ids.amount',
        'machine_total_cost',
    )
    def _compute_mrp_costs(self):
        for rec in self:
            rec.mrp_labor_cost    = sum(rec.labor_line_ids.mapped('total_cost'))
            rec.mrp_overhead_cost = sum(rec.overhead_line_ids.mapped('amount'))
            rec.mrp_grand_total   = (
                rec.machine_total_cost
                + rec.mrp_labor_cost
                + rec.mrp_overhead_cost
            )

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _mfg_get_account(self, param_name):
        param = self.env['ir.config_parameter'].sudo().get_param(param_name)
        if param:
            return self.env['account.account'].browse(int(param)).exists()
        return self.env['account.account']

    def _mfg_get_journal(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'manufacturing_machines.machine_journal_id')
        if param:
            journal = self.env['account.journal'].browse(int(param)).exists()
            if journal:
                return journal
        return self.env['account.journal'].search([('type', '=', 'general')], limit=1)

    # ── Actions ───────────────────────────────────────────────────────────────
    def action_mrp_post_accounting(self):
        """Post a journal entry for all production costs (machines + labor + overhead)"""
        self.ensure_one()
        if self.mrp_cost_posted:
            raise UserError('The accounting entry has already been posted!')
        if not self.mrp_grand_total:
            raise UserError('There are no costs to post!')

        journal = self._mfg_get_journal()
        if not journal:
            raise UserError('No journal found — please configure one in Manufacturing Settings.')

        machine_account  = self._mfg_get_account('manufacturing_machines.machine_cost_account_id')
        labor_account    = self._mfg_get_account('manufacturing_machines.labor_cost_account_id')
        overhead_account = self._mfg_get_account('manufacturing_machines.overhead_cost_account_id')
        contra_account   = self._mfg_get_account('manufacturing_machines.contra_account_id')

        if not contra_account:
            raise UserError(
                'Please set the Contra (credit) account in Manufacturing Settings before posting!'
            )

        lines = []
        if self.machine_total_cost and machine_account:
            lines.append((0, 0, {
                'name': f'Machine cost – {self.name}',
                'account_id': machine_account.id,
                'debit': self.machine_total_cost,
                'credit': 0.0,
            }))
        if self.mrp_labor_cost and labor_account:
            lines.append((0, 0, {
                'name': f'Labor cost – {self.name}',
                'account_id': labor_account.id,
                'debit': self.mrp_labor_cost,
                'credit': 0.0,
            }))
        if self.mrp_overhead_cost and overhead_account:
            lines.append((0, 0, {
                'name': f'Overhead costs – {self.name}',
                'account_id': overhead_account.id,
                'debit': self.mrp_overhead_cost,
                'credit': 0.0,
            }))

        if not lines:
            raise UserError(
                'No cost accounts are configured. '
                'Please set them in Manufacturing → Configuration → Settings.'
            )

        total_debit = sum(l[2]['debit'] for l in lines)
        lines.append((0, 0, {
            'name': f'Total production cost – {self.name}',
            'account_id': contra_account.id,
            'debit': 0.0,
            'credit': total_debit,
        }))

        move = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': journal.id,
            'date': fields.Date.today(),
            'ref': f'Manufacturing Order: {self.name}',
            'line_ids': lines,
        })
        move.action_post()
        self.mrp_move_id = move
        self.mrp_cost_posted = True

    def action_view_mrp_journal_entry(self):
        """Open the linked accounting journal entry"""
        self.ensure_one()
        if not self.mrp_move_id:
            raise UserError('No journal entry found for this order.')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Journal Entry',
            'res_model': 'account.move',
            'res_id': self.mrp_move_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _mfg_get_or_create_lc_product(self, name):
        """Find or create a service product to use as a landed cost line product."""
        Product = self.env['product.product'].sudo()
        product = Product.search([('name', '=', name), ('type', '=', 'service')], limit=1)
        if not product:
            product = Product.create({
                'name': name,
                'type': 'service',
                'invoice_policy': 'order',
                'purchase_ok': False,
                'sale_ok': False,
            })
        return product

    def action_create_landed_cost(self):
        """Create a Landed Cost entry pre-filled with all production costs,
        linked to this manufacturing order (target_model = manufacturing)."""
        self.ensure_one()
        if 'stock.landed.cost' not in self.env:
            raise UserError(
                'The Landed Costs module (stock_landed_costs) is not installed.\n'
                'Please install it from the Apps menu first.'
            )

        if not self.mrp_grand_total:
            raise UserError('There are no costs to create a landed cost for!')

        # Accounts from settings
        machine_account  = self._mfg_get_account('manufacturing_machines.machine_cost_account_id')
        labor_account    = self._mfg_get_account('manufacturing_machines.labor_cost_account_id')
        overhead_account = self._mfg_get_account('manufacturing_machines.overhead_cost_account_id')

        cost_lines = []

        if self.machine_total_cost:
            product = self._mfg_get_or_create_lc_product('Machine Operating Cost')
            line_vals = {
                'product_id': product.id,
                'name': f'Machine cost – {self.name}',
                'price_unit': self.machine_total_cost,
                'split_method': 'by_current_cost_price',
            }
            if machine_account:
                line_vals['account_id'] = machine_account.id
            cost_lines.append((0, 0, line_vals))

        if self.mrp_labor_cost:
            product = self._mfg_get_or_create_lc_product('Labor Cost')
            line_vals = {
                'product_id': product.id,
                'name': f'Labor cost – {self.name} ({len(self.labor_line_ids)} workers)',
                'price_unit': self.mrp_labor_cost,
                'split_method': 'by_current_cost_price',
            }
            if labor_account:
                line_vals['account_id'] = labor_account.id
            cost_lines.append((0, 0, line_vals))

        if self.mrp_overhead_cost:
            product = self._mfg_get_or_create_lc_product('Overhead Cost')
            line_vals = {
                'product_id': product.id,
                'name': f'Overhead – {self.name} ({len(self.overhead_line_ids)} items)',
                'price_unit': self.mrp_overhead_cost,
                'split_method': 'equal',
            }
            if overhead_account:
                line_vals['account_id'] = overhead_account.id
            cost_lines.append((0, 0, line_vals))

        landed = self.env['stock.landed.cost'].sudo().create({
            'target_model': 'manufacturing',
            'mrp_production_ids': [(4, self.id)],
            'cost_lines': cost_lines,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Landed Cost',
            'res_model': 'stock.landed.cost',
            'res_id': landed.id,
            'view_mode': 'form',
            'target': 'current',
        }
