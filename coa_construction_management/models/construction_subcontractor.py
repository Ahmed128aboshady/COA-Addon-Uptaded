# -*- coding: utf-8 -*-
""" Construction Subcontractor """
from odoo import api, fields, models, _


class ConstructionSubcontractor(models.Model):
    """ Construction Subcontractor """
    _name = 'construction.subcontractor'
    _description = 'Construction Subcontractor'

    name = fields.Char(default='New')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('attribution_done', 'Attribution Done'),
                              ('project_in_progress', 'Project In Progress'), (
                                  'interim_invoice_created',
                                  'Interim Invoice Created'), ('lock', 'Lock')],
                             default='draft')

    partner_id = fields.Many2one('res.partner', string="Vendor")
    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    construction_subcontractor_lines_ids = fields.One2many(
        'construction.subcontractor.lines', 'construction_subcontractor_id')

    date = fields.Date(default=fields.Date.today())
    attribution_type = fields.Selection(
        [('complete_boq', 'Complete BOQ'), ('part_boq', 'Part BOQ')])
    boq_cost_estimation_id = fields.Many2one('boq.cost.estimation',
                                             domain="[('state','in',['approved','project_in_progress']),('project_id','=',construction_project_id)]")
    bill_of_quantities_id = fields.Many2one('detailed.bill.of.quantities',
                                            domain="[('boq_cost_estimation_id','=',boq_cost_estimation_id)]")
    project_id = fields.Many2one('project.project')
    interim_invoice_ids = fields.One2many('interim.invoice', 'construction_subcontractor_id')
    count_interim_invoice = fields.Integer(compute='_compute_construction_interim_invoice', store=True)
    # analytic_account_id = fields.Many2one('account.analytic.account')



    @api.depends('interim_invoice_ids')
    def _compute_construction_interim_invoice(self):
        """ Compute count_move_line  value """
        for rec in self:
            rec.count_interim_invoice = len(
                rec.interim_invoice_ids.ids)

    def action_view_all_interim_invoice(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "interim.invoice",
            "domain": [('construction_subcontractor_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Interim Invoice"),
            'view_mode': 'list,form',
        }
        return result

    def lock(self):
        """ Lock """
        for rec in self:
            rec.state = 'lock'

    def start_project(self):
        """ Create Project """
        for rec in self:
            # analytic = self.env['account.analytic.account'].sudo().create(
            #     {'name': rec.project_name + "/" + rec.project_number,
            #      'plan_id': self.env.ref(
            #          'analytic.analytic_plan_projects').id}).id
            # rec.analytic_account_id = analytic
            project = self.env['project.project'].sudo().create(
                {
                    'name': rec.construction_project_id.project_name + "/" + rec.name,
                    'partner_id': rec.partner_id.id,
                    'construction_project_id': rec.construction_project_id.id,
                    'project_number': rec.construction_project_id.project_number,
                    'project_description': rec.construction_project_id.project_description,
                    'project_type_id': rec.construction_project_id.project_type_id.id,
                    'project_manager_id': rec.construction_project_id.employee_id.id,

                    'type_ids': [
                        (4, self.env.ref('arabian_construction_management.project_stage_0').id),
                        (4, self.env.ref('arabian_construction_management.project_stage_1').id),
                        (4, self.env.ref('arabian_construction_management.project_stage_2').id),
                        (4, self.env.ref('arabian_construction_management.project_stage_3').id)

                    ],

                    # 'analytic_account_id': analytic
                }).id

            for a in self.construction_subcontractor_lines_ids:
                tasks = self.env['project.task'].sudo().create(
                    {
                    # 'boq_cost_estimation_id': a.id,
                     'business_item_id': a.business_item_id.id,
                     'name': a.bill_quantities_labour_machines_id.name,
                     'business_items_types_id': a.business_items_types_id.id,
                     'description': a.description, 'uom_id': a.uom_id.id,
                     'quantity': a.quantity,
                     'project_name': rec.project_name,
                     'construction_project_id': rec.construction_project_id.id,
                     'project_number': rec.construction_project_id.project_number,
                     'project_description': rec.construction_project_id.project_description,
                     'project_type_id': rec.construction_project_id.project_type_id.id,
                     'project_manager_id': rec.construction_project_id.employee_id.id,
                     'stage_id': self.env.ref("arabian_construction_management.project_stage_0").id,
                     'project_id': project,
                     # 'analytic_account_id': analytic
                     })
            rec.project_id = project
            rec.state = 'project_in_progress'

    def create_interim_invoice(self):
        """ Create Interim Invoice """

        items = []
        for rec in self.construction_subcontractor_lines_ids:
            items.append((0, 0, {
                'bill_quantities_labour_machines_id': rec.bill_quantities_labour_machines_id.id,
                'product_id': rec.product_id.id,
                'boq_cost_estimation_line_id': rec.boq_cost_estimation_line_id.id,
                'business_item_id': rec.business_item_id.id,
                'business_items_types_id': rec.business_items_types_id.id,
                'name': rec.description,
                'uom_id': rec.uom_id.id,
                'boq_quantity': rec.quantity}))
        self.env['interim.invoice'].sudo().create(
            {'construction_subcontractor_id': self.id,
             'interim_type': 'subcontractor_interim',
             'attribution_type': self.attribution_type,
             'partner_id': self.partner_id.id,
             'construction_project_id': self.construction_project_id.id,
             'project_name': self.project_name,
             'project_number': self.project_number,
             'interim_invoice_line_ids': items})
        self.state = 'interim_invoice_created'

    @api.onchange('construction_project_id')
    def _onchange_construction_project_id(self):
        """ construction_project_id """
        for rec in self:
            if rec.construction_project_id:
                rec.project_name = rec.construction_project_id.project_name
                rec.project_number = rec.construction_project_id.project_number

    def confirm(self):
        """ Confirm """
        for rec in self:
            rec.state = 'confirm'

    def attribution(self):
        """ Attribution """
        items = []
        if self.attribution_type == 'complete_boq':
            for rec in self.boq_cost_estimation_id.boq_cost_estimation_ids:
                items.append((0, 0, {
                    'boq_cost_estimation_line_id': rec.id,
                    'business_item_id': rec.business_item_id.id,
                    'business_items_types_id': rec.business_items_types_id.id,
                    'description': rec.description,
                    'item_price': rec.rate,
                    'currency_id': rec.currency_id.id,
                    'uom_id': rec.uom_id.id,
                    'previous_qty': rec.total_qty,
                    'quantity': rec.quantity
                }))
                rec.previous_qty += rec.current_qty
                rec.current_qty = 0
        elif self.attribution_type == 'part_boq':
            for rec in self.bill_of_quantities_id.bill_quantities_labour_machines_ids:
                items.append((0, 0, {
                    'bill_quantities_labour_machines_id': rec.id,
                    'productivity_per_unit_item': rec.productivity_per_unit_item,
                    'product_id': rec.product_id.id,
                    'name': rec.description,
                    'working_hours': rec.working_hours,
                    'uom_id': rec.uom_id.id,
                    'unit_price': rec.unit_price,
                    'total_cost': rec.subtotal,
                    'currency_id': rec.currency_id.id,
                    'cost_per_item_unit': rec.cost_per_item_unit,
                }))

            for rec in self.bill_of_quantities_id.bill_quantities_overhead_ids:
                items.append((0, 0, {
                    'bill_quantities_overhead_machines_id': rec.id,
                    'productivity_per_unit_item': rec.productivity_per_unit_item,
                    'product_id': rec.product_id.id,
                    'name': rec.name,
                    'uom_id': rec.uom_id.id,
                    'quantity': rec.quantity,
                    'unit_price': rec.unit_price,
                    'total_cost': rec.subtotal,
                    'currency_id': rec.currency_id.id,
                    'cost_per_item_unit': rec.cost_per_item_unit,
                }))

            for rec in self.bill_of_quantities_id.bill_of_quantities_line_ids:
                items.append((0, 0, {
                    'bill_quantities_machines_id': rec.id,
                    'productivity_per_unit_item': rec.productivity_per_unit_item,
                    'product_id': rec.product_id.id,
                    'name': rec.name,
                    'uom_id': rec.uom_id.id,
                    'unit_price': rec.unit_price,
                    'total_cost': rec.subtotal,
                    'currency_id': rec.currency_id.id,
                    'cost_per_item_unit': rec.cost_per_item_unit,
                }))

        action = self.env.ref('arabian_construction_management.subcontractor_attribution_boq_action').sudo().read()[0]
        action['context'] = {
            'default_subcontractor_attribution_boq_line_ids': items,
            'default_attribution_type': self.attribution_type
        }
        action['views'] = [
            (self.env.ref('arabian_construction_management.subcontractor_attribution_boq_form').id, 'form')]
        return action

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.subcontractor') or '/'
        return super(ConstructionSubcontractor, self).create(vals)


class ConstructionSubcontractorLines(models.Model):
    """ Construction Subcontractor Lines """
    _name = 'construction.subcontractor.lines'
    _description = 'Construction Subcontractor Lines'

    construction_subcontractor_id = fields.Many2one(
        'construction.subcontractor')
    construction_business_items_id = fields.Many2one(
        'construction.business.items')
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    product_id = fields.Many2one('product.product')
    description = fields.Text(translate=True)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    quantity = fields.Float(default=1)
    rate = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    total_cost = fields.Monetary(currency_field='currency_id', compute="_compute_total_cost",readonly=0,store=True)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',
                                                  string="code")
    bill_quantities_labour_machines_id = fields.Many2one(
        'bill.quantities.labour.machines', string="code")
    bill_quantities_overhead_machines_id = fields.Many2one(
        'bill.quantities.overhead')
    bill_quantities_machines_id = fields.Many2one(
        'bill.of.quantities.line')
    previous_qty = fields.Float(string="Previous QTY")
    current_qty = fields.Float(string="Current QTY")
    total_qty = fields.Float(string="Total QTY", compute='_compute_total_qty',
                             store=True)

    @api.depends('rate', 'quantity')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.rate * rec.quantity

    @api.depends('previous_qty', 'current_qty')
    def _compute_total_qty(self):
        """ Compute total_qty value """
        for rec in self:
            rec.total_qty = rec.current_qty + rec.previous_qty
