# -*- coding: utf-8 -*-
from odoo import _, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    retention_account_id = fields.Many2one(
        "account.account",
        string="Retention Receivable Account",
        domain="[('account_type', '=', 'asset_receivable'),"
               " ('deprecated', '=', False)]",
        help="Dedicated receivable-type account where the retained portion "
             "of customer invoices is posted. MUST be of type Receivable so "
             "it appears correctly in the Partner Ledger and Aged "
             "Receivable reports.",
    )
    retention_default_percent = fields.Float(
        string="Default Retention (%)",
        default=10.0,
        help="Default retention percentage proposed on new sales orders. "
             "Can be changed on each order/contract.",
    )
    retention_default_period_days = fields.Integer(
        string="Default Retention Period (Days)",
        default=365,
        help="Default number of days after delivery until the retention "
             "becomes due. Can be changed on each order/contract.",
    )
    retention_default_base = fields.Selection(
        [
            ("total", "Total (VAT Included)"),
            ("untaxed", "Untaxed Amount (Before VAT)"),
        ],
        string="Default Retention Base",
        default="total",
        required=True,
        help="Default amount the retention percentage is applied to. "
             "Can be changed on each order/contract.",
    )

    def action_open_retention_lines(self):
        """Open all journal items posted on the retention account
        (used by the Accounting menu entry)."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Retention Receivables"),
            "res_model": "account.move.line",
            "view_mode": "list,form",
            "domain": [
                ("account_id", "=", self.retention_account_id.id),
                ("parent_state", "=", "posted"),
            ],
            "context": {
                "search_default_group_by_partner": 1,
                "search_default_unreconciled": 1,
            },
        }
