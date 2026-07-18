from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_accrued_expense = fields.Boolean(
        string='Accrued',
        help="Tick to spread this expense line over a period as an accrued "
             "expense (distinct from a Deferred expense).",
    )
    accrued_start_date = fields.Date(string='Accrual Start')
    accrued_end_date = fields.Date(string='Accrual End')

    # Stores the original expense account when we swap it to the accrual
    # account on posting. Restored automatically when the bill goes back to draft.
    accrued_expense_account_id = fields.Many2one(
        'account.account',
        string='Original Expense Account (Accrual)',
        copy=False,
        help='Set automatically on posting: holds the original expense account '
             'while the line uses the accrual account.',
    )
