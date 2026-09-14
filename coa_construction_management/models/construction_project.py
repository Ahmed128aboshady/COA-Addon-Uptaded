# -*- coding: utf-8 -*-
""" Construction Project """
from odoo import api, fields, models, _
from datetime import date, datetime
import dateutil


class ConstructionProject(models.Model):
    """ Construction Project """
    _name = 'construction.project'
    _description = 'Construction Project'

    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'),
         ('business_items_created', 'Business Items Created'),
         ('assay_approved', 'Assay Approved'),
         ('assay_rejected', 'Assay Rejected'),
         ('project_in_progress', 'Project In Progress'),
         ('cancelled', 'Cancelled')],
        string="Status", default='draft')
    name = fields.Char(default='New')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_description = fields.Html(translate=True)
    project_type_id = fields.Many2one('construction.project.type')
    partner_id = fields.Many2one('res.partner', string="Customer")
    project_location = fields.Char(translate=True)
    project_start_date = fields.Date()
    expected_completion_date = fields.Date()
    project_duration = fields.Char(compute='_compute_expected_completion',
                                   store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    total_budget = fields.Monetary(currency_field='currency_id')
    expected_cost_project = fields.Monetary(currency_field='currency_id',
                                            string="Expected cost of the project")

    business_item_ids = fields.One2many(
        'construction.business.items',
        'project_id',
        string="Business Items"
    )

    current_costs_to_date = fields.Monetary(
        currency_field='currency_id',
        string="Current Costs (To Date)",
        compute="_compute_current_costs_to_date",
        store=True
    )
    percentage_financial_achievement = fields.Float(
        string="Percentage of financial achievement")
    allocated_costs_materials = fields.Monetary(currency_field='currency_id',
                                                string="Allocated costs for materials")
    labor_costs = fields.Monetary(currency_field='currency_id')
    equipment_costs = fields.Monetary(currency_field='currency_id')

    employee_id = fields.Many2one('hr.employee', string="Project Manager")
    main_contractor_id = fields.Many2one('res.partner',
                                         string="Main Contractor")
    subcontractors_ids = fields.Many2many('res.partner')

    current_number_workers = fields.Integer()

    count_construction_business_items = fields.Integer(
        compute='_compute_construction_business_items',
        store=True)

    construction_business_items_ids = fields.One2many(
        'construction.business.items', 'project_id')
    business_items_created = fields.Boolean()
    project_project_ids = fields.One2many('project.project',
                                          'construction_project_id')
    count_project = fields.Integer(compute='_compute_count_project', store=True)
    analytic_account_id = fields.Many2one('account.analytic.account')
    contract_type = fields.Selection(
        [('tender', 'Tender'), ('attribution_direct', 'Attribution direct'),
         ('other', 'Other')])
    other_contract_type = fields.Char()
    tender_no = fields.Char()
    site_area = fields.Char()
    account_payment_ids = fields.One2many('account.payment',
                                          'construction_project_id')
    count_payment = fields.Integer(compute='_compute_count_payment', store=True)

    expense_payment_ids = fields.One2many('expense.payment',
                                          'construction_project_id')
    count_expense_payment = fields.Integer(
        compute='_compute_count_expense_payment', store=True)
    incoming_cheque_ids = fields.One2many('incoming.cheque',
                                          'construction_project_id')
    outgoing_cheque_ids = fields.One2many('outgoing.cheque',
                                          'construction_project_id')
    incoming_cheque_count = fields.Integer(
        compute='_compute_incoming_cheque_count', store=True)
    outgoing_cheque_count = fields.Integer(
        compute='_compute_outgoing_cheque_count', store=True)
    bid_bond_ids = fields.One2many('lg.bid.bond', 'construction_project_id')
    count_bid_bond = fields.Integer(compute='_compute_count_bid_bond',
                                    store=True)
    boq_cost_estimation_id = fields.Many2one('boq.cost.estimation',
                                             string="Assay")
    project_contract_account_id = fields.Many2one('account.account')
    terms_account_id = fields.Many2one('account.account')
    terms_amount = fields.Float()
    project_contract_journal_id = fields.Many2one('account.journal')
    documents_folder_id = fields.Many2one('documents.document')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    sale_id = fields.Many2one('sale.order', string="SO")
    sale = fields.Boolean(string="Sale")

    @api.depends('business_item_ids.breakdown_ids.item_total_vat_margin')
    def _compute_current_costs_to_date(self):
        for project in self:
            total = 0.0
            for business_item in project.business_item_ids:
                for breakdown in business_item.breakdown_ids:
                    total += breakdown.item_total_vat_margin or 0.0
            project.current_costs_to_date = total

    def action_view_related_so(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "domain": [('construction_ids', 'in', self.ids)],
            "context": {"create": False},
            "name": _("Related Sale Orders"),
            "view_mode": 'list,form',
        }

    @api.depends('bid_bond_ids')
    def _compute_count_bid_bond(self):
        """ Compute count_bid_bond value """
        for rec in self:
            rec.count_bid_bond = len(rec.bid_bond_ids.ids)

    def action_view_all_bid_bond(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "lg.bid.bond",
            "domain": [('construction_project_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Incoming Cheque"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('incoming_cheque_ids')
    def _compute_incoming_cheque_count(self):
        """ Compute incoming_cheque_count value """
        for rec in self:
            rec.incoming_cheque_count = len(rec.incoming_cheque_ids.ids)

    def action_view_all_incoming_cheque(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "incoming.cheque",
            "domain": [('construction_project_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Incoming Cheque"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('outgoing_cheque_ids')
    def _compute_outgoing_cheque_count(self):
        """ Compute outgoing_cheque_count value """
        for rec in self:
            rec.outgoing_cheque_count = len(rec.outgoing_cheque_ids.ids)

    def action_view_all_outgoing_cheque(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "outgoing.cheque",
            "domain": [('construction_project_id', '=', self.id)],
            "context": {"create": False},
            "name": _("outgoing Cheque"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('expense_payment_ids')
    def _compute_count_expense_payment(self):
        """ Compute count_expense_payment value """
        for rec in self:
            rec.count_expense_payment = len(rec.expense_payment_ids.ids)

    def action_view_all_expense_payment(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "expense.payment",
            "domain": [('construction_project_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Expense"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('account_payment_ids')
    def _compute_count_payment(self):
        """ Compute count_payment value """
        for rec in self:
            rec.count_payment = len(rec.account_payment_ids.ids)

    def action_view_all_account_payment(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.payment",
            "domain": [('construction_project_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Payment"),
            'view_mode': 'kanban,list,form',
        }
        return result

    def action_view_all_construction_project(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "domain": [('construction_project_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Project"),
            'view_mode': 'kanban,list,form',
        }
        return result

    @api.depends('project_project_ids')
    def _compute_count_project(self):
        """ Compute project value """
        for rec in self:
            rec.count_project = len(rec.project_project_ids.ids)

    def start_project(self):
        """ Create Project """

        for rec in self:

            analytic = self.env['account.analytic.account'].sudo().create(
                {'name': rec.project_name + "/" + rec.project_number,
                 'plan_id': self.env.ref(
                     'analytic.analytic_plan_projects').id}).id
            rec.analytic_account_id = analytic

            project = self.env['project.project'].sudo().create(
                {'name': rec.project_name, 'partner_id': rec.partner_id.id,
                 'construction_project_id': rec.id,
                 'project_number': rec.project_number,
                 'project_description': rec.project_description,
                 'project_type_id': rec.project_type_id.id,
                 'project_manager_id': rec.employee_id.id,

                 'type_ids': [(4, self.env.ref('arabian_construction_management.project_stage_0').id),
                              (4, self.env.ref('arabian_construction_management.project_stage_1').id),
                              (4, self.env.ref('arabian_construction_management.project_stage_2').id),
                              (4, self.env.ref('arabian_construction_management.project_stage_3').id)

                              ],

                 # 'analytic_account_id': analytic
                 }).id
            approved_assay = self.env['boq.cost.estimation'].sudo().search(
                [('state', '=', 'approved')], limit=1)
            if approved_assay:
                for a in approved_assay.boq_cost_estimation_ids:
                    tasks = self.env['project.task'].sudo().create(
                        {'boq_cost_estimation_id': a.boq_cost_estimation_id.id,
                         'boq_cost_estimation_line_id': a.id,
                         'name': a.name,
                         'business_item_id': a.business_item_id.id,
                         'business_items_types_id': a.business_items_types_id.id,
                         'description': a.description, 'uom_id': a.uom_id.id,
                         'quantity': a.quantity,
                         'project_name': rec.project_name,
                         'construction_project_id': rec.id,
                         'project_number': rec.project_number,
                         'project_description': rec.project_description,
                         'project_type_id': rec.project_type_id.id,
                         'project_manager_id': rec.employee_id.id,
                         'stage_id': self.env.ref("arabian_construction_management.project_stage_0").id,
                         'project_id': project,
                         # 'analytic_account_id': analytic
                         })
            rec.state = 'project_in_progress'
            rec.boq_cost_estimation_id.state = 'project_in_progress'
            if rec.contract_type == 'tender':
                lines = [(0, 0,
                          {
                              'account_id': rec.terms_account_id.id,
                              'debit': 0.0,
                              'credit': rec.terms_amount,
                              'analytic_distribution': {str(rec.analytic_account_id.id): 100},
                              'name': "مصاريف كراسة الشروط بعد رسو العطاء"}),
                         (0, 0, {
                             'account_id': rec.project_contract_account_id.id,
                             'credit': 0.0, 'debit': rec.terms_amount,

                             'analytic_distribution': {str(rec.analytic_account_id.id): 100},
                             'name': "مصاريف كراسة الشروط بعد رسو العطاء"})]
                account_move = self.env['account.move'].sudo().create(
                    {'journal_id': rec.project_contract_journal_id.id,
                     'line_ids': lines,
                     'construction_project_id': rec.id,
                     'project_name': rec.project_name,
                     'project_number': rec.project_number,
                     'move_type': 'entry'})
                account_move.action_post()

    @api.depends('construction_business_items_ids')
    def _compute_construction_business_items(self):
        """ Compute count_move_line  value """
        for rec in self:
            rec.count_construction_business_items = len(
                rec.construction_business_items_ids.ids)

    def action_view_all_construction_business_items(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "construction.business.items",
            "domain": [('project_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Construction Business Items"),
            'view_mode': 'list,form',
        }
        return result

    def confirm(self):
        """ Confirm """
        for rec in self:
            rec.state = 'confirmed'

    def create_business_items(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_construction_management.create_business_items_action').sudo().read()[
            0]
        action['views'] = [(self.env.ref(
            'arabian_construction_management.create_business_items_form').id,
                            'form')]
        return action

    def create_payment_request(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_construction_management.construction_project_payment_action').sudo().read()[
            0]
        action['views'] = [(self.env.ref(
            'arabian_construction_management.construction_project_payment_form').id,
                            'form')]
        return action

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.project') or '/'

        project_name = vals.get('project_name', vals.get('name'))
        if project_name:
            vals['documents_folder_id'] = self.env['documents.document'].create({
                'name': project_name,
                'folder_id': self.env.ref(
                    'arabian_construction_management.construction_documents_folder').id
            }).id

        return super(ConstructionProject, self).create(vals)

    @api.depends('expected_completion_date', 'project_start_date')
    def _compute_expected_completion(self):
        """ Compute birthday value """
        for rec in self:
            date = fields.Date.from_string(rec.project_start_date)
            # Get the current date

            now = fields.Date.from_string(rec.expected_completion_date)
            # Get the difference between the current date and the birthday
            age = dateutil.relativedelta.relativedelta(now, date)
            # age = age.years
            rec.project_duration = " year " + str(age.years) + " month " + str(
                age.months) + " day " + str(age.days)
