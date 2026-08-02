# -*- coding: utf-8 -*-
""" Expense Payment """
from odoo import api, fields, models, _


class ExpensePayment(models.Model):
    """ Expense Payment """
    _name = 'expense.payment'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Expense Payment'

    def _default_tax(self):
        if self.env.company.account_purchase_tax_id:
            return [(4, self.env.company.account_purchase_tax_id.id)]



    state = fields.Selection([('1', 'Draft'), ('2', 'Posted')], default='1',
                             string="Status")
    name = fields.Char(default='New')
    payment_type = fields.Selection([('1', 'Send'), ('2', 'Receive')])
    total_amount = fields.Monetary(currency_field='currency_id', tracking=True,
                                   compute='_compute_total_amount', store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id,
                                  tracking=True)
    memo = fields.Char(tracking=True)
    date = fields.Date(default=fields.Date.today(), tracking=True)
    journal_id = fields.Many2one('account.journal',
                                 domain=[('type', 'in', ['bank', 'cash']),
                                         ('allow_expense', '=', True)],
                                 tracking=True)

    count_expense_payment = fields.Integer(compute='_compute_expense_payment',
                                           store=True, string="Journal Entry")
    account_move_ids = fields.One2many('account.move', 'expense_payment_id')

    tax_value = fields.Float()
    amount_with_tax = fields.Float()
    reference = fields.Char()
    already_created = fields.Boolean()

    expense_payment_line_ids = fields.One2many('expense.payment.line',
                                               'expense_payment_id')
    total_taxes_amount = fields.Monetary(compute='_compute_total_amount',
                                         store=True,
                                         currency_field='currency_id')
    note = fields.Html()
    total_after_tax = fields.Monetary(compute='_compute_total_amount',
                                      store=True, currency_field='currency_id')
    company_id = fields.Many2one('res.company',default=lambda self: self.env.company)
    user_company_ids = fields.Many2many('res.company')

    analytic_precision = fields.Integer(store=False,
                                        default=lambda self: self.env[
                                            'decimal.precision'].precision_get(
                                            "Percentage Analytic"))
    analytic_distribution = fields.Json(compute='_compute_get_analytic_distribution', store=True)

    @api.depends('expense_payment_line_ids')
    def _compute_get_analytic_distribution(self):
        """Compute analytic_distribution value without duplicates."""
        for rec in self:
            all_distributions = []
            for line in rec.expense_payment_line_ids:
                if line.analytic_distribution:
                    all_distributions.append(line.analytic_distribution)

            merged_distribution = {}
            for dist in all_distributions:
                for account, value in dist.items():
                    merged_distribution[account] = merged_distribution.get(account, 0) + value
            rec.analytic_distribution = merged_distribution



    def reset_to_draft(self):
        """ Reset To Draft """
        for rec in self:
            rec.state = '1'
            if rec.account_move_ids:
                for i in rec.account_move_ids:
                    i.button_draft()

    def _get_report_base_filename(self):
        self.ensure_one()
        return self.name

    @api.depends('expense_payment_line_ids')
    def _compute_total_amount(self):
        """ Compute total+ value """
        for rec in self:

            total_amount = 0
            total_taxes_amount = 0
            for line in rec.expense_payment_line_ids:
                total_amount += line.amount
                total_taxes_amount += line.tax_amount
            rec.update({
                'total_amount': total_amount,
                'total_taxes_amount': total_taxes_amount,
                'total_after_tax': total_amount - total_taxes_amount
            })

    # @api.depends('tax_ids', 'amount')
    # def _compute_amount_with_tax(self):
    #     """ Compute amount_with_tax value """
    #     for rec in self:
    #         rec.tax_value = 0
    #         tax_value = 0
    #         rec.amount_with_tax = rec.amount
    #         if rec.tax_ids and rec.amount > 0:
    #             for t in rec.tax_ids:
    #                 tax_value = t.amount
    #                 rec.tax_value += (tax_value * rec.amount) / 100
    #             rec.amount_with_tax = rec.tax_value + rec.amount

    @api.depends('account_move_ids')
    def _compute_expense_payment(self):
        """ Compute expense_payment value """
        for rec in self:
            rec.count_expense_payment = len(rec.account_move_ids.ids)

    def view_account_pay(self):
        """ View Account Pay """

        recs = self.mapped('account_move_ids')
        action = \
            self.env.ref(
                'account.action_move_journal_line').sudo().read()[0]
        if len(recs) > 1:
            action['domain'] = [('id', 'in', recs.ids)]

        elif len(recs) == 1:
            action['views'] = [
                (
                    self.env.ref('account.view_move_form').id,
                    'form')]
            action['res_id'] = recs.ids[0]

        else:
            action['views'] = [
                (
                    self.env.ref('account.view_move_form').id,
                    'form')]

        return action

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'expense.payment') or '/'
        return super(ExpensePayment, self).create(vals)

    def confirm(self):
        """ Confirm """
        tag_ids = []
        debit_line = {}
        credit_line = {}
        tax_line = []
        recs = []
        lines = []
        accounts = []

        if not self.already_created:
            for rec in self.expense_payment_line_ids:
                if rec.tax_ids:
                    for t in rec.tax_ids:
                        for g in t.invoice_repartition_line_ids:
                            if g.account_id and g.repartition_type == 'tax':

                                lines.append((0, 0, {
                                    'account_id': g.account_id.id,
                                    'name': t.name,
                                    'debit': (rec.amount * t.amount) / (100+rec.tax_included),
                                    'credit': 0,
                                    'currency_id': rec.currency_id.id,
                                    'employee_id': rec.employee_id.id,
                                    'date_maturity': self.date,
                                    'analytic_distribution': rec.analytic_distribution,
                                    'tax_tag_ids': g.tag_ids.ids,
                                    'partner_id':rec.partner_id.id
                                }))
                                print("accounts", g.account_id.id)
                                accounts.append(g.account_id.id)
                                print("accounts", accounts)
                            else:
                                if g.tag_ids:
                                    tag_ids = []
                                    for h in g.tag_ids:
                                        tag_ids.append(h.id)
                print("tax_line", rec.amount - rec.tax_amount)
                lines.append((0, 0, {
                    'account_id':
                        rec.account_id.id,
                    'name': 'Expense Payment ' + self.name + ' ' + str(
                        rec.amount) + rec.currency_id.name + ' / ' + str(
                        self.date),
                    'debit': rec.amount - rec.tax_amount,
                    'credit': 0,
                    'currency_id': rec.currency_id.id,
                    'expense_payment_id': self.id,
                    'expense_payment_line_id': rec.id,
                    'date_maturity': self.date,
                    'employee_id': rec.employee_id.id,
                    'memo': rec.memo,
                    'tax_tag_ids': [(6, 0, tag_ids)],
                    'analytic_distribution': rec.analytic_distribution,
                    'partner_id':rec.partner_id.id

                }))
            lines.append((0, 0, {
                'account_id': self.journal_id.default_account_id.id,
                'name': 'Expense Payment ' + self.name + ' ' + str(
                    self.total_amount) + self.currency_id.name + ' / ' + str(
                    self.date),
                'debit': 0,
                'credit': self.total_amount,
                'expense_payment_id': self.id,
                'currency_id': self.currency_id.id,
                'date_maturity': self.date,
                'analytic_distribution':self.analytic_distribution
            }))

            move_vals = {
                'date': self.date,
                'expense_payment_id': self.id,
                'journal_id': self.journal_id.id,
                'ref': self.reference,
                'currency_id': self.currency_id.id,
                'move_type': 'entry',
                'line_ids': lines
            }
            move_id = self.env['account.move'].sudo().create(move_vals)
            move_id.sudo().action_post()
            self.sudo().write({'state': '2', 'already_created': True})
        else:
            items = []
            self.account_move_ids[0].line_ids = False
            for rec in self.expense_payment_line_ids:
                if rec.tax_ids:
                    for t in rec.tax_ids:
                        for g in t.invoice_repartition_line_ids:
                            if g.account_id and g.repartition_type == 'tax':

                                lines.append((0, 0, {
                                    'account_id': g.account_id.id,
                                    'name': t.name,
                                    'debit': (rec.amount * t.amount) / (100+rec.tax_included),
                                    'credit': 0,
                                    'currency_id': rec.currency_id.id,
                                    'date_maturity': self.date,
                                    'employee_id': rec.employee_id.id,
                                    'analytic_distribution': rec.analytic_distribution,
                                    'tax_tag_ids': g.tag_ids.ids,
                                    'partner_id':rec.partner_id.id
                                }))
                                print("accounts", g.account_id.id)
                                accounts.append(g.account_id.id)
                                print("accounts", accounts)
                            else:
                                if g.tag_ids:
                                    tag_ids = []
                                    for h in g.tag_ids:
                                        tag_ids.append(h.id)
                print("tax_line", tag_ids)
                lines.append((0, 0, {
                    'account_id':
                        rec.account_id.id,
                    'name': 'Expense Payment ' + self.name + ' ' + str(
                        rec.amount) + rec.currency_id.name + ' / ' + str(
                        self.date),
                    'debit': rec.amount - rec.tax_amount,
                    'credit': 0,
                    'currency_id': rec.currency_id.id,
                    'expense_payment_id': self.id,
                    'expense_payment_line_id': rec.id,
                    'date_maturity': self.date,
                    'employee_id': rec.employee_id.id,
                    'memo': rec.memo,
                    'tax_tag_ids': [(6, 0, tag_ids)],
                    'analytic_distribution': rec.analytic_distribution,
                    'partner_id':rec.partner_id.id

                }))
            lines.append((0, 0, {
                'account_id': self.journal_id.default_account_id.id,
                'name': 'Expense Payment ' + self.name + ' ' + str(
                    self.total_amount) + self.currency_id.name + ' / ' + str(
                    self.date),
                'debit': 0,
                'credit': self.total_amount,
                'expense_payment_id': self.id,
                'currency_id': self.currency_id.id,
                'date_maturity': self.date,
                'analytic_distribution':self.analytic_distribution
            }))

            account_move = self.env['account.move'].sudo().search(
                [('expense_payment_id', '=', self.id)], limit=1)
            account_move.sudo().write({'date': self.date,
                                'expense_payment_id': self.id,
                                'journal_id': self.journal_id.id,
                                'ref': self.reference,
                                'currency_id': self.currency_id.id,
                                'move_type': 'entry',
                                'line_ids': lines})

            account_move.sudo().action_post()
            self.sudo().write({'state': '2'})


class ExpensePaymentLine(models.Model):
    """ Expense Payment Line """
    _name = 'expense.payment.line'
    _description = 'Expense Payment Line'

    expense_payment_id = fields.Many2one('expense.payment')
    product_id = fields.Many2one('product.product',
                                 domain=[('type', '=', 'service')])
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  related='expense_payment_id.currency_id')
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
    price_after_tax = fields.Float(compute='_compute_price_after_taxx', store=True)

    @api.depends('tax_included','amount','tax_amount')
    def _compute_price_after_taxx(self):
        """ Compute price_after_tax value """
        for rec in self:
            rec.price_after_tax = rec.amount-rec.tax_amount

    @api.depends('amount', 'tax_ids', 'product_id','tax_included')
    def _compute_tax_amount(self):
        """ Compute tax_amount value """
        for rec in self:
            rec.tax_amount = 0
            if rec.tax_ids and rec.amount > 0:
                for t in rec.tax_ids:
                    rec.tax_amount += (rec.amount * t.amount) / (100+rec.tax_included)
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
