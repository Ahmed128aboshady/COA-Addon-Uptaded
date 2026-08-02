# -*- coding: utf-8 -*-
""" Boq Cost Estimation """
from odoo import api, fields, models, _


class BoqCostEstimation(models.Model):
    """ Boq Cost Estimation """
    _name = 'boq.cost.estimation'
    _description = 'BOQ Cost Estimation'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('project_in_progress', 'Project In-Progress'),
        ('interim_invoice_created', 'Interim Invoice Created'),
        ('lock', 'Lock'),
    ], string='Status', default='draft')
    name = fields.Char(default='New')
    construction_business_items_id = fields.Many2one(
        'construction.business.items')
    project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_description = fields.Html(translate=True)
    project_type_id = fields.Many2one('construction.project.type')
    partner_id = fields.Many2one('res.partner', string="Customer")
    project_location = fields.Char(translate=True)
    date = fields.Date()

    boq_cost_estimation_ids = fields.One2many('boq.cost.estimation.line',
                                              'boq_cost_estimation_id')
    total = fields.Monetary(currency_field='currency_id',
                            compute='_compute_total', store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    note = fields.Html()
    interim_invoice_ids = fields.One2many('interim.invoice', 'assay_id')
    count_interim_invoice = fields.Integer(
        compute='_compute_construction_interim_invoice', store=True)

    def lock(self):
        """ Lock """
        for rec in self:
            rec.state = 'lock'

    def create_interim_invoice(self):
        """ Create Interim Invoice """

        items = []
        for rec in self.boq_cost_estimation_ids:
            items.append((0, 0, {
                'boq_cost_estimation_line_id': rec.id,
                'business_item_id': rec.business_item_id.id,
                'business_items_types_id': rec.business_items_types_id.id,
                'name': rec.description,
                'uom_id': rec.uom_id.id,
                'boq_quantity': rec.quantity,
                'item_price': rec.rate,
                'previous_qty': rec.total_qty,
                'currency_id': rec.currency_id.id,
            }))
            rec.previous_qty+=rec.current_qty
            rec.current_qty=0
        self.env['interim.invoice'].sudo().create(
            {'assay_id': self.id,
             'interim_type': 'owner_interim',
             'attribution_type': 'complete_boq',
             'partner_id': self.partner_id.id,
             'construction_project_id': self.project_id.id,
             'project_name': self.project_name,
             'project_number': self.project_number,
             'interim_invoice_line_ids': items})
        self.state = 'interim_invoice_created'

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
            "domain": [('assay_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Interim Invoice"),
            'view_mode': 'list,form',
        }
        return result

    def approved(self):
        """ Approved """
        for rec in self:
            rec.state = 'approved'
            rec.project_id.state = 'assay_approved'
            rec.project_id.boq_cost_estimation_id=rec.id

    def rejected(self):
        """ Rejected """
        for rec in self:
            rec.state = 'rejected'
            rec.project_id.state = 'assay_rejected'

    def confirm(self):
        """ Confirm """
        for rec in self:
            rec.state = 'confirm'

    @api.depends('boq_cost_estimation_ids')
    def _compute_total(self):
        """ Compute total value """
        for rec in self:
            rec.total = 0
            for t in rec.boq_cost_estimation_ids:
                rec.total += t.total_cost

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'boq.cost.estimation') or '/'
        return super(BoqCostEstimation, self).create(vals)


class BoqCostEstimationLine(models.Model):
    """ Boq Cost Estimation Line """
    _name = 'boq.cost.estimation.line'
    _description = 'Boq Cost Estimation Line'

    name = fields.Char(string="Item Code")
    boq_cost_estimation_id = fields.Many2one('boq.cost.estimation')
    detailed_bill_of_quantities_id = fields.Many2one(
        'detailed.bill.of.quantities', string="Detailed BOQ")
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    description = fields.Text(translate=True)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    quantity = fields.Float(default=1)
    rate = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    total_cost = fields.Monetary(currency_field='currency_id')
    construction_business_items_id = fields.Many2one(
        'construction.business.items')
    previous_qty = fields.Float(string="Previous QTY")
    current_qty = fields.Float(string="Current QTY")
    total_qty = fields.Float(string="Total QTY", compute='_compute_total_qty',
                             store=True)
    item_code = fields.Char()

    @api.depends('previous_qty', 'current_qty')
    def _compute_total_qty(self):
        """ Compute total_qty value """
        for rec in self:
            rec.total_qty = rec.current_qty + rec.previous_qty

    @api.onchange('business_item_id')
    def _onchange_business_item_id(self):
        """ business_item_id """
        for rec in self:
            if rec.business_item_id:
                rec.business_items_types_id = rec.business_item_id.business_items_types_id.id
                rec.uom_id = rec.business_item_id.uom_id.id
