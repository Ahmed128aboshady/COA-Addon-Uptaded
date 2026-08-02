# -*- coding: utf-8 -*-
""" Interim Completion Certificate """
from odoo import api, fields, models, _


class InterimInvoice(models.Model):
    """ Interim Invoice """
    _name = 'interim.invoice'
    _description = 'Interim Invoice'

    name = fields.Char(default='New')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('invoice_created', 'Invoice Created'),('bill_created', 'Bill Created')],
                             default='draft')
    reference = fields.Char()
    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_description = fields.Html(translate=True)
    project_type_id = fields.Many2one('construction.project.type')
    partner_id = fields.Many2one('res.partner')
    project_location = fields.Char(translate=True)
    from_date = fields.Date()
    to_date = fields.Date()
    assay_id = fields.Many2one('boq.cost.estimation')
    registration_date = fields.Date(default=fields.Date.today())
    note = fields.Html()
    interim_invoice_line_ids = fields.One2many('interim.invoice.line',
                                               'interim_invoice_id')
    interim_invoice_deductions_ids = fields.One2many(
        'interim.invoice.deductions', 'interim_invoice_id')
    total_works = fields.Monetary(currency_field='currency_id',
                                  compute='_compute_total_works', store=True)
    total_current_works = fields.Monetary(currency_field='currency_id',
                                          compute='_compute_total_works')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    total_works_note = fields.Html()
    works_after_deduction = fields.Monetary(currency_field='currency_id',
                                            compute='_compute_works_after_deduction',
                                            store=True)
    current_works_after_deduction = fields.Monetary(
        currency_field='currency_id',
        compute='_compute_works_after_deduction')
    total_deduction_note = fields.Html()
    construction_subcontractor_id = fields.Many2one(
        'construction.subcontractor')

    account_move_ids = fields.One2many('account.move', 'interim_invoice_id')
    count_invoice = fields.Integer(compute='_compute_account_move', store=True)
    interim_type = fields.Selection([('owner_interim', 'Owner Interim'), (
        'subcontractor_interim', 'Subcontractor Interim')])
    attribution_type = fields.Selection(
        [('complete_boq', 'Complete BOQ'), ('part_boq', 'Part BOQ')],
        default='complete_boq')

    def confirm(self):
        """ Confirm """
        for rec in self:
            rec.state = 'confirm'

    @api.depends('account_move_ids')
    def _compute_account_move(self):
        """ Compute count_move_line  value """
        for rec in self:
            rec.count_invoice = len(
                rec.account_move_ids.ids)

    def action_view_all_interim_invoice(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('interim_invoice_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Account Move"),
            'view_mode': 'list,form',
        }
        return result

    def create_invoice(self):
        """ Create Invoice """
        items = []
        for rec in self.interim_invoice_line_ids:
            items.append((0, 0, {'name': rec.name, 'quantity': 1,
                                 'price_unit': rec.current_subtotal}))
            rec.boq_cost_estimation_line_id.current_qty = rec.current_qty
            rec.boq_cost_estimation_line_id.previous_qty = rec.previous_qty
        for rec2 in self.interim_invoice_deductions_ids:
            items.append((0, 0, {'name': rec2.name, 'quantity': 1,
                                 'price_unit': -1 * rec2.current_deduction_value}))
        self.env['account.move'].sudo().create(
            {'interim_invoice_id': self.id, 'partner_id': self.partner_id.id,
             'invoice_date':fields.Date.today(),
             'move_type': 'out_invoice',
             'invoice_line_ids': items})
        self.state = 'invoice_created'

    def create_bill(self):
        """ Create Invoice """
        items = []
        for rec in self.interim_invoice_line_ids:
            items.append((0, 0, {'name': rec.name, 'quantity': 1,
                                 'price_unit': rec.current_subtotal}))
            rec.construction_subcontractor_lines_id.current_qty = rec.current_qty
            rec.construction_subcontractor_lines_id.previous_qty = rec.previous_qty
        for rec2 in self.interim_invoice_deductions_ids:
            items.append((0, 0, {'name': rec2.name, 'quantity': 1,
                                 'price_unit': -1 * rec2.current_deduction_value}))
        self.env['account.move'].sudo().create(
            {'interim_invoice_id': self.id, 'partner_id': self.partner_id.id,
             'move_type': 'in_invoice',
             'invoice_line_ids': items})
        self.state = 'bill_created'

    @api.depends('interim_invoice_line_ids')
    def _compute_total_works(self):
        """ Compute total_works value """
        for rec in self:
            rec.total_works = 0
            rec.total_current_works = 0
            for rec2 in rec.interim_invoice_line_ids:
                rec.total_works += rec2.subtotal
                rec.total_current_works += rec2.current_subtotal

    @api.depends('interim_invoice_line_ids', 'interim_invoice_deductions_ids',
                 'total_works', 'total_current_works')
    def _compute_works_after_deduction(self):
        """ Compute works_after_deduction value """
        for rec in self:
            rec.works_after_deduction = 0
            rec.current_works_after_deduction = 0
            for rec2 in rec.interim_invoice_deductions_ids:
                rec.works_after_deduction = rec.total_works - rec2.deduction_value
                rec.current_works_after_deduction = rec.total_current_works - rec2.current_deduction_value

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'interim.invoice') or '/'
        return super(InterimInvoice, self).create(vals)


class InterimInvoiceLine(models.Model):
    """ Interim Invoice Line """
    _name = 'interim.invoice.line'
    _description = 'Interim Invoice Line'

    interim_invoice_id = fields.Many2one('interim.invoice')
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    product_id = fields.Many2one('product.product')
    name = fields.Text(translate=True, string="Description")
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    previous_qty = fields.Float(string="Previous QTY")
    current_qty = fields.Float(string="Current QTY")
    total_qty = fields.Float(string="Total QTY", compute='_compute_total_qty',
                             store=True)
    item_price = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    progress = fields.Integer(string="Progress %")
    subtotal = fields.Monetary(currency_field='currency_id',
                               compute='_compute_subtotal', store=True)
    current_subtotal = fields.Monetary(currency_field='currency_id',
                                       compute='_compute_subtotal',
                                       store=True, )
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',
                                                  string="code")
    bill_quantities_labour_machines_id = fields.Many2one(
        'bill.quantities.labour.machines', string="code")

    boq_quantity = fields.Float(string="BOQ Quantity")
    construction_subcontractor_lines_id = fields.Many2one('construction.subcontractor.lines')

    @api.depends('current_qty', 'previous_qty')
    def _compute_total_qty(self):
        """ Compute total_qty value """
        for rec in self:
            rec.total_qty = rec.previous_qty + rec.current_qty

    @api.depends('progress', 'total_qty', 'item_price', 'current_qty',
                 'previous_qty')
    def _compute_subtotal(self):
        """ Compute subtotal value """
        for rec in self:
            rec.subtotal = rec.progress * rec.total_qty * rec.item_price
            rec.current_subtotal = rec.progress * rec.current_qty * rec.item_price


class InterimInvoiceDeductions(models.Model):
    """ Interim Invoice Deductions """
    _name = 'interim.invoice.deductions'
    _description = 'Interim Invoice Deductions'

    interim_invoice_id = fields.Many2one('interim.invoice')
    name = fields.Char()
    amount = fields.Float(digits=(16, 0))
    type = fields.Selection([('percentage', 'Percentage'), ('value', 'Value')],
                            default='percentage')
    current_deduction_value = fields.Float(compute='_compute_deduction_value',
                                           store=True)
    deduction_value = fields.Float(compute='_compute_deduction_value',
                                   store=True)
    total_works = fields.Monetary(currency_field='currency_id',
                                  compute='_compute_total_works', store=True,
                                  related='interim_invoice_id.total_works')
    total_current_works = fields.Monetary(currency_field='currency_id',
                                          related='interim_invoice_id.total_current_works',
                                          store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)

    @api.depends('amount', 'type', 'total_works', 'total_current_works')
    def _compute_deduction_value(self):
        """ Compute deduction_value value """
        for rec in self:
            if rec.type == 'percentage':
                rec.deduction_value = rec.total_works * rec.amount / 100
                rec.current_deduction_value = rec.total_current_works * rec.amount / 100
            elif rec.type == 'value':
                rec.deduction_value = rec.amount
                rec.current_deduction_value = rec.amount
