# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    retention_percent = fields.Float(
        string="Retention (%)",
        copy=False,
        tracking=True,
        help="Percentage of the invoice total held as retention. "
             "Comes from the sales order; can be adjusted while draft.",
    )
    retention_period_days = fields.Integer(
        string="Retention Period (Days)",
        copy=False,
        help="Days after delivery until the retained amount becomes due.",
    )
    retention_base = fields.Selection(
        [
            ("total", "Total (VAT Included)"),
            ("untaxed", "Untaxed Amount (Before VAT)"),
        ],
        string="Retention Base",
        default="total",
        copy=False,
        help="Amount the retention percentage is applied to. "
             "Comes from the sales order; can be adjusted while draft.",
    )
    retention_amount = fields.Monetary(
        string="Retention Amount",
        compute="_compute_retention_amount",
    )
    retention_due_date = fields.Date(
        string="Retention Due Date",
        compute="_compute_retention_due_date",
        store=True,
        readonly=False,
        copy=False,
        help="Maturity date of the retained amount. Automatically proposed "
             "as (last delivery date + retention period); can be adjusted "
             "manually before posting.",
    )
    retention_move_id = fields.Many2one(
        "account.move",
        string="Retention Entry",
        readonly=True,
        copy=False,
        help="Journal entry moving the retained amount from the trade "
             "receivable account to the dedicated retention account.",
    )

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------
    def _get_retention_base_amount(self):
        self.ensure_one()
        return (
            self.amount_untaxed
            if self.retention_base == "untaxed"
            else self.amount_total
        )

    @api.depends("amount_total", "amount_untaxed",
                 "retention_percent", "retention_base")
    def _compute_retention_amount(self):
        for move in self:
            move.retention_amount = move.currency_id.round(
                move._get_retention_base_amount()
                * (move.retention_percent or 0.0) / 100.0
            )

    @api.depends("retention_period_days", "invoice_date", "state")
    def _compute_retention_due_date(self):
        for move in self:
            if move.retention_due_date and move.state != "draft":
                continue  # never recompute once posted
            if not move.retention_percent:
                move.retention_due_date = False
                continue
            base_date = move._get_retention_base_date()
            move.retention_due_date = base_date + timedelta(
                days=move.retention_period_days or 0
            )

    def _get_retention_base_date(self):
        """Base date for maturity: last validated outgoing delivery of the
        related sale order(s); fallback to invoice date, then today."""
        self.ensure_one()
        sale_orders = self.invoice_line_ids.sale_line_ids.order_id
        done_deliveries = sale_orders.picking_ids.filtered(
            lambda p: p.picking_type_code == "outgoing" and p.state == "done"
        )
        dates = [d for d in done_deliveries.mapped("date_done") if d]
        if dates:
            return max(dates).date()
        return self.invoice_date or fields.Date.context_today(self)

    # ------------------------------------------------------------------
    # Posting hook
    # ------------------------------------------------------------------
    def _post(self, soft=True):
        posted = super()._post(soft=soft)
        for move in posted:
            if (
                move.move_type == "out_invoice"
                and move.retention_percent
                and not move.retention_move_id
            ):
                move._create_retention_entry()
        return posted

    def _create_retention_entry(self):
        """Create + post + reconcile the retention reclass entry:

            DR  Retention Receivable      (maturity = delivery + period)
            CR  Trade Receivable          (reconciled against the invoice)

        The invoice itself is untouched (legal total and VAT intact); the
        open trade receivable becomes total - retention, and the retained
        amount lives in the dedicated account with its own maturity so the
        Aged Receivable and Partner Ledger report it correctly.
        """
        self.ensure_one()
        company = self.company_id
        retention_account = company.retention_account_id
        if not retention_account:
            raise UserError(_(
                "No Retention Receivable Account is configured.\n"
                "Set it under Accounting → Settings → Customer Retention."
            ))
        if retention_account.account_type != "asset_receivable":
            raise UserError(_(
                "The retention account '%(account)s' must be of type "
                "'Receivable' so it appears correctly in the Partner Ledger "
                "and Aged Receivable reports.",
                account=retention_account.display_name,
            ))

        receivable_lines = self.line_ids.filtered(
            lambda l: l.display_type == "payment_term"
        )
        if not receivable_lines:
            return

        amount = self.currency_id.round(
            self._get_retention_base_amount() * self.retention_percent / 100.0
        )
        if self.currency_id.is_zero(amount):
            return

        ar_account = receivable_lines[0].account_id
        partner = self.commercial_partner_id
        conv_date = self.invoice_date or fields.Date.context_today(self)
        balance = self.currency_id._convert(
            amount, company.currency_id, company, conv_date
        )
        due_date = self.retention_due_date or (
            self._get_retention_base_date()
            + timedelta(days=self.retention_period_days or 0)
        )

        ref = _(
            "Retention %(pct)s%% on %(inv)s",
            pct=self.retention_percent, inv=self.name,
        )
        retention_move = self.env["account.move"].create({
            "move_type": "entry",
            "journal_id": self.journal_id.id,
            "date": conv_date,
            "ref": ref,
            "line_ids": [
                Command.create({
                    "name": ref,
                    "account_id": retention_account.id,
                    "partner_id": partner.id,
                    "currency_id": self.currency_id.id,
                    "amount_currency": amount,
                    "debit": balance,
                    "credit": 0.0,
                    "date_maturity": due_date,
                }),
                Command.create({
                    "name": ref,
                    "account_id": ar_account.id,
                    "partner_id": partner.id,
                    "currency_id": self.currency_id.id,
                    "amount_currency": -amount,
                    "debit": 0.0,
                    "credit": balance,
                    "date_maturity": conv_date,
                }),
            ],
        })
        retention_move._post(soft=False)
        self.retention_move_id = retention_move

        # Reconcile the credit line with the invoice's receivable line(s)
        # so the open trade receivable drops to (total - retention).
        credit_line = retention_move.line_ids.filtered(
            lambda l: l.account_id == ar_account and l.credit > 0
        )
        (credit_line + receivable_lines).reconcile()

    # ------------------------------------------------------------------
    # Draft/cancel: keep the retention entry consistent with the invoice
    # ------------------------------------------------------------------
    def button_draft(self):
        res = super().button_draft()
        for move in self:
            retention = move.retention_move_id
            if retention and retention.state == "posted":
                retention.line_ids.remove_move_reconcile()
                retention.button_draft()
                retention.button_cancel()
                move.retention_move_id = False
        return res

    def action_open_retention_move(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": self.retention_move_id.id,
        }
