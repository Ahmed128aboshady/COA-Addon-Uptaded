from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    accrued_expense_account_id = fields.Many2one(
        related='company_id.accrued_expense_account_id',
        string='Accrued Expense Account',
        readonly=False,
    )
    accrued_expense_journal_id = fields.Many2one(
        related='company_id.accrued_expense_journal_id',
        string='Accrued Expense Journal',
        readonly=False,
    )
