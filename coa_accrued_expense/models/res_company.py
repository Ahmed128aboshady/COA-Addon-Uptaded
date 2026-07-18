from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    accrued_expense_account_id = fields.Many2one(
        'account.account',
        string='Accrued Expense Account',
        domain="[('deprecated', '=', False)]",
        help="Intermediate account used to hold the expense until it is "
             "recognized month by month.",
    )
    accrued_expense_journal_id = fields.Many2one(
        'account.journal',
        string='Accrued Expense Journal',
        domain="[('type', '=', 'general')]",
        help="Journal in which the accrual and recognition entries are booked.",
    )
