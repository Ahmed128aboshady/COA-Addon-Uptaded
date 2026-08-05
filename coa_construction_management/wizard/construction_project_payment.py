# -*- coding: utf-8 -*-
""" Construction Project Payment """
from odoo import api, fields, models, _


class ConstructionProjectPayment(models.TransientModel):
    """ Construction Project Payment """
    _name = 'construction.project.payment'
    _description = 'Construction Project Payment'

    type = fields.Selection(
        [('normal_payment', 'Normal Payment'), ('cheque', 'Cheque'),
         ('letter_of_guarantee', 'Letter Of Guarantee'),
         ('expense', 'Expense')], default='normal_payment')
    partner_id = fields.Many2one('res.partner')
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    memo = fields.Char()
    date = fields.Date(default=fields.Date.today())
    payment_type = fields.Selection(
        [('outbound', 'Send'), ('inbound', 'Receive')], default='outbound')
    journal_id = fields.Many2one('account.journal',
                                 domain="[('type','in',['cash','bank'])]")
    cheque_type = fields.Selection(
        [('incoming', 'Incoming'), ('outgoing', 'Outgoing')])
    description = fields.Text()
    beneficiary = fields.Char()
    cheque_number = fields.Char()

    expiry_date = fields.Date()
    beneficiary_name = fields.Char()
    beneficiary_address = fields.Char()
    guarantee_details = fields.Html()
    guarantee_for = fields.Selection(
        [('bid_bond', 'Bid Bond'), ('performance_bond', 'Performance Bond'), (
            'advance_payment_guarantee', 'Advance Payment Guarantee'),
         ('maintenance_bond', 'Maintenance Bond')])
    construction_expense_line_ids = fields.One2many('construction.expense.line',
                                                    'construction_project_payment_id')
    company_id = fields.Many2one('res.company',default=lambda self: self.env.company)

    def confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        construction_project = self.env['construction.project'].browse(
            active_id)
        for rec in self:
            if rec.type == 'normal_payment':
                self.env['account.payment'].sudo().create(
                    {'partner_id': rec.partner_id.id, 'amount': rec.amount,
                     'currency_id': rec.currency_id.id, 'memo': rec.memo,
                     'payment_type': rec.payment_type,
                     'journal_id': rec.journal_id.id,
                     'construction_project_id': construction_project.id,
                     'project_name': construction_project.project_name,
                     'project_number': construction_project.project_number})
            elif rec.type == 'cheque':
                if rec.cheque_type == 'incoming':
                    self.env['incoming.cheque'].sudo().create(
                        {'partner_id': rec.partner_id.id, 'amount': rec.amount,
                         'currency_id': rec.currency_id.id,
                         'description': rec.description,
                         'construction_project_id': construction_project.id,
                         'project_name': construction_project.project_name,
                         'project_number': construction_project.project_number,
                         'beneficiary': rec.beneficiary,
                         'cheque_number': rec.cheque_number,
                         })
                elif rec.cheque_type == 'outgoing':
                    self.env['outgoing.cheque'].sudo().create(
                        {'partner_id': rec.partner_id.id, 'amount': rec.amount,
                         'currency_id': rec.currency_id.id,
                         'description': rec.description,
                         'construction_project_id': construction_project.id,
                         'project_name': construction_project.project_name,
                         'project_number': construction_project.project_number,
                         'beneficiary': rec.beneficiary,
                         'cheque_number': rec.cheque_number,
                         })
            elif rec.type == 'letter_of_guarantee':
                if rec.guarantee_for == 'bid_bond':
                    self.env['lg.bid.bond'].sudo().create(
                        {'partner_id': rec.partner_id.id,
                         'guarantee_amount': rec.amount,
                         'currency_id': rec.currency_id.id,
                         'description': rec.description,
                         'construction_project_id': construction_project.id,
                         'project_name': construction_project.project_name,
                         'project_number': construction_project.project_number,
                         'beneficiary_name': rec.beneficiary_name,
                         'tender_no': construction_project.tender_no,
                         'date': rec.date,
                         'expiry_date': rec.expiry_date,
                         'beneficiary_address': rec.beneficiary_address,
                         'guarantee_details': rec.guarantee_details,
                         })
                elif rec.guarantee_for == 'performance_bond':
                    self.env['lg.performance.bond'].sudo().create(
                        {'partner_id': rec.partner_id.id,
                         'guarantee_amount': rec.amount,
                         'currency_id': rec.currency_id.id,
                         'description': rec.description,
                         'construction_project_id': construction_project.id,
                         'project_name': construction_project.project_name,
                         'project_number': construction_project.project_number,
                         'beneficiary_name': rec.beneficiary_name,
                         'tender_no': construction_project.tender_no,
                         'date': rec.date,
                         'expiry_date': rec.expiry_date,
                         'beneficiary_address': rec.beneficiary_address,
                         'guarantee_details': rec.guarantee_details,
                         })
                elif rec.guarantee_for == 'advance_payment_guarantee':
                    self.env['lg.advance.payment.guarantee'].sudo().create(
                        {'partner_id': rec.partner_id.id,
                         'guarantee_amount': rec.amount,
                         'currency_id': rec.currency_id.id,
                         'description': rec.description,
                         'construction_project_id': construction_project.id,
                         'project_name': construction_project.project_name,
                         'project_number': construction_project.project_number,
                         'beneficiary_name': rec.beneficiary_name,
                         'tender_no': construction_project.tender_no,
                         'date': rec.date,
                         'expiry_date': rec.expiry_date,
                         'beneficiary_address': rec.beneficiary_address,
                         'guarantee_details': rec.guarantee_details,
                         })
                elif rec.guarantee_for == 'maintenance_bond':
                    self.env['lg.maintenance.bond'].sudo().create(
                        {'partner_id': rec.partner_id.id,
                         'guarantee_amount': rec.amount,
                         'currency_id': rec.currency_id.id,
                         'description': rec.description,
                         'construction_project_id': construction_project.id,
                         'project_name': construction_project.project_name,
                         'project_number': construction_project.project_number,
                         'beneficiary_name': rec.beneficiary_name,
                         'tender_no': construction_project.tender_no,
                         'date': rec.date,
                         'expiry_date': rec.expiry_date,
                         'beneficiary_address': rec.beneficiary_address,
                         'guarantee_details': rec.guarantee_details,
                         })
            elif rec.type == 'expense':
                items = []
                for i in rec.construction_expense_line_ids:
                    items.append((0, 0, {'product_id': i.product_id.id,
                                         'partner_id': i.partner_id.id,
                                         'employee_id': i.employee_id.id,
                                         'amount': i.amount,
                                         'memo': i.memo,
                                         'account_id': i.account_id.id,
                                         'analytic_distribution': i.analytic_distribution,
                                         'tax_ids': i.tax_ids.ids}))
                    construction_project.terms_account_id = i.account_id.id
                    construction_project.terms_amount = i.amount
                self.env['expense.payment'].sudo().create(
                    {'currency_id': rec.currency_id.id,
                     'company_id':rec.company_id.id,
                     'journal_id': rec.journal_id.id,
                     'payment_type':'1',
                     'construction_project_id': construction_project.id,
                     'project_name': construction_project.project_name,
                     'project_number': construction_project.project_number,
                     'expense_payment_line_ids': items})


class ConstructionExpenseLine(models.TransientModel):
    """ Construction Expense Line """
    _name = 'construction.expense.line'
    _description = 'Construction Expense Line'

    construction_project_payment_id = fields.Many2one(
        'construction.project.payment')
    product_id = fields.Many2one('product.product',
                                 domain=[('type', '=', 'service')])
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  related='construction_project_payment_id.currency_id')
    account_id = fields.Many2one('account.account', tracking=True, domain=[
        ('account_type', 'in', ['expense', 'expense_direct_cost'])])
    employee_id = fields.Many2one('hr.employee')
    analytic_precision = fields.Integer(store=False,
                                        default=lambda self: self.env[
                                            'decimal.precision'].precision_get(
                                            "Percentage Analytic"))
    analytic_distribution = fields.Json()
    memo = fields.Char(string="Description")

    tax_ids = fields.Many2many('account.tax',
                               domain=[('type_tax_use', '=', 'purchase')])
    tax_amount = fields.Float(compute='_compute_tax_amount', store=True)
    partner_id = fields.Many2one('res.partner')
    tax_included = fields.Float(default=15)
    price_after_tax = fields.Float(compute='_compute_price_after_taxx',
                                   store=True)

    @api.depends('tax_included', 'amount', 'tax_amount')
    def _compute_price_after_taxx(self):
        """ Compute price_after_tax value """
        for rec in self:
            rec.price_after_tax = rec.amount - rec.tax_amount

    @api.depends('amount', 'tax_ids', 'product_id', 'tax_included')
    def _compute_tax_amount(self):
        """ Compute tax_amount value """
        for rec in self:
            rec.tax_amount = 0
            if rec.tax_ids and rec.amount > 0:
                for t in rec.tax_ids:
                    rec.tax_amount += (rec.amount * t.amount) / (
                            100 + rec.tax_included)
                    print("rec.tax_amount on line", rec.tax_amount)
                print("rec.tax_amount", rec.tax_amount)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.account_id = False
            rec.tax_ids = False
            if rec.product_id:
                rec.account_id = rec.product_id.property_account_expense_id.id
                rec.tax_ids = rec.product_id.supplier_taxes_id.ids
