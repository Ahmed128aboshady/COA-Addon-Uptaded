# -*- coding: utf-8 -*-
"""
COA Journal Dashboard – GL Balance  (v2)
=========================================
Replaces the split bank/cash dashboard balance with a single number taken
directly from the General Ledger (posted account_move_line on the journal's
default account).

v2 additions:
  • Always shows nb_lines_bank_account_balance as an integer (not bool) so the
    template condition  `> 0`  works correctly.
  • For journals that have their own foreign currency (e.g. a USD bank account
    inside an EGP company), we show TWO lines:
        – Line 1 (account_balance)           → amount in FOREIGN currency (USD)
        – Line 2 (outstanding_pay_account_balance) → same amount converted to
          COMPANY currency (EGP), labelled via nb_lines_outstanding_pay_account_balance=1
    This mirrors the behaviour users expect and keeps the kanban template
    completely untouched (no JS/XML overrides needed).
  • Secondary misc / payments lines are always suppressed (already in GL).
"""

from odoo import _, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # ------------------------------------------------------------------
    # Helper: GL balance from account_move_line
    # ------------------------------------------------------------------

    def _coa_get_gl_balance(self):
        """Return a dict  {journal_id: row_dict}  with:

            gl_balance_currency   – sum of amount_currency  (journal currency)
            gl_balance_company    – sum of balance           (company currency)
            line_count            – number of posted AML rows on default acct
        """
        if not self:
            return {}

        # Balance source, per journal, with a fallback so a journal never
        # shows an empty balance while it actually has posted entries:
        #   1. If the journal has a default account -> sum posted items on
        #      that account. This ties out exactly to the official General
        #      Ledger report (posted account.move.line on the account).
        #   2. Otherwise -> sum every posted item recorded in the journal
        #      itself (journal_id), which is the closest equivalent to the
        #      GL filtered on that journal.
        self.env.cr.execute("""
            SELECT j.id                                     AS journal_id,
                   COALESCE(SUM(aml.amount_currency), 0.0) AS gl_balance_currency,
                   COALESCE(SUM(aml.balance),         0.0) AS gl_balance_company,
                   COUNT(aml.id)                            AS line_count
              FROM account_journal j
         LEFT JOIN account_move_line aml
                    ON aml.parent_state = 'posted'
                   AND aml.company_id = ANY(%(companies)s)
                   AND (
                        (j.default_account_id IS NOT NULL
                         AND aml.account_id = j.default_account_id)
                     OR (j.default_account_id IS NULL
                         AND aml.journal_id = j.id)
                   )
             WHERE j.id = ANY(%(journals)s)
          GROUP BY j.id
        """, {
            'companies': self.env.companies.ids,
            'journals': self.ids,
        })

        return {row['journal_id']: row for row in self.env.cr.dictfetchall()}

    # ------------------------------------------------------------------
    # Override: replace bank/cash dashboard data with GL balance
    # ------------------------------------------------------------------

    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        """After standard fill, replace balance lines with GL balance."""
        super()._fill_bank_cash_dashboard_data(dashboard_data)

        bank_cash_journals = self.filtered(
            lambda j: j.type in ('bank', 'cash', 'credit'))
        if not bank_cash_journals:
            return

        gl_data = bank_cash_journals._coa_get_gl_balance()
        company_currency = self.env.company.sudo().currency_id

        for journal in bank_cash_journals:
            row = gl_data.get(journal.id, {})
            gl_balance_currency = row.get('gl_balance_currency', 0.0)
            gl_balance_company  = row.get('gl_balance_company',  0.0)
            line_count          = int(row.get('line_count', 0))

            # Journal currency (foreign) vs company currency
            j_currency = journal.currency_id  # False if same as company

            accessible = (
                journal.company_id.id
                in journal.company_id._accessible_branches().ids
            )

            has_lines = line_count > 0

            if j_currency and j_currency != company_currency:
                # ── Foreign-currency journal (e.g. USD bank in EGP company) ─
                # Line 1: GL balance in journal's own currency (e.g. USD)
                # Line 2: same amount in company currency    (e.g. EGP)
                dashboard_data[journal.id].update({
                    # Primary balance in foreign currency
                    'account_balance': j_currency.format(gl_balance_currency),
                    'nb_lines_bank_account_balance': line_count if (has_lines and accessible) else 0,

                    # Secondary line = company-currency equivalent
                    'outstanding_pay_account_balance': company_currency.format(gl_balance_company),
                    'nb_lines_outstanding_pay_account_balance': 1 if (has_lines and accessible) else 0,

                    # Suppress misc line (already consolidated in GL)
                    'nb_misc_operations': 0,
                    'misc_operations_balance': None,
                })
            else:
                # ── Same-currency journal (normal case) ───────────────────
                # Single line in company currency
                dashboard_data[journal.id].update({
                    'account_balance': company_currency.format(gl_balance_company),
                    'nb_lines_bank_account_balance': line_count if (has_lines and accessible) else 0,

                    # Suppress both secondary lines
                    'outstanding_pay_account_balance': company_currency.format(0),
                    'nb_lines_outstanding_pay_account_balance': 0,

                    'nb_misc_operations': 0,
                    'misc_operations_balance': None,
                })
