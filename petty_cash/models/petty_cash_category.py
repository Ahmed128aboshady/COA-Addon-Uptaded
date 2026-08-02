from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


class PettyCashCategory(models.Model):
    _name = 'petty.cash.category'
    _description = 'Petty Cash Expense Category'
    _order = 'sequence, name'

    name = fields.Char(string='Category Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    code = fields.Char(string='Code', size=10)
    account_id = fields.Many2one(
        'account.account',
        string='Expense Account',
        required=True,
        help='Debit account when approving an expense from this category',
        domain="[('account_type', 'in', ["
               "'expense', 'expense_depreciation', "
               "'expense_direct_cost'])]",
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Cost Center',
        help='Default cost center for this category (optional)',
    )
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
    expense_ids = fields.One2many(
        'petty.cash.expense',
        'category_id',
        string='Expenses'
    )
    expense_count = fields.Integer(
        string='Expenses Count',
        compute='_compute_expense_count'
    )
    total_amount = fields.Monetary(
        string='Total Expenses',
        compute='_compute_expense_count',
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('expense_ids', 'expense_ids.state', 'expense_ids.amount')
    def _compute_expense_count(self):
        for rec in self:
            approved = rec.expense_ids.filtered(lambda e: e.state == 'approved')
            rec.expense_count = len(approved)
            rec.total_amount = sum(approved.mapped('amount'))

    def action_view_expenses(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Expenses of %s') % self.name,
            'res_model': 'petty.cash.expense',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
        }
