from odoo import models, fields


class PettyCashConfig(models.TransientModel):
    """Petty Cash Settings - res.config.settings"""
    _inherit = 'res.config.settings'

    # ── Accounts ────────────────────────────────────────────────────────────
    petty_cash_account_id = fields.Many2one(
        'account.account',
        string='Petty Cash Account',
        help='Debit account when granting custody to employee (usually cash or custody account)',
        config_parameter='petty_cash.account_id',
        domain="[('account_type', 'in', ['asset_cash', 'asset_current'])]",
    )
    petty_cash_payment_account_id = fields.Many2one(
        'account.account',
        string='Default Cash/Bank Account',
        help='Default cash/bank account when disbursing custody - can be changed per custody',
        config_parameter='petty_cash.payment_account_id',
        domain="[('account_type', 'in', ['asset_cash', 'asset_current', 'liability_current'])]",
    )

    # ── Approval settings ───────────────────────────────────────────────────
    petty_cash_require_manager_approval = fields.Boolean(
        string='Require Manager Approval for Large Custodies',
        help='If enabled, custodies exceeding the set limit require manager approval before processing',
        config_parameter='petty_cash.require_manager_approval',
    )
    petty_cash_manager_approval_limit = fields.Float(
        string='Manager Approval Amount Limit',
        help='Custodies exceeding this amount require manager approval',
        config_parameter='petty_cash.manager_approval_limit',
    )
    petty_cash_custody_approver_id = fields.Many2one(
        'res.users',
        string='Default Custody Approver',
        help='User who receives custody approval request notifications',
        config_parameter='petty_cash.custody_approver_id',
    )
    petty_cash_expense_approver_id = fields.Many2one(
        'res.users',
        string='Default Expense Approver',
        help='User who receives expense approval request notifications',
        config_parameter='petty_cash.expense_approver_id',
    )
