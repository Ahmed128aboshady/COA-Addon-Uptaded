# -*- coding: utf-8 -*-
import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)

_PURCHASE_TYPES = ('in_invoice', 'in_refund')
_SALE_TYPES     = ('out_invoice', 'out_refund')

# Marker used to identify our injected cost lines
_COA_LINE_MARKER = '[COA-COGS]'


class AccountMove(models.Model):
    _inherit = 'account.move'

    # ------------------------------------------------------------------
    # _post(): inject cost lines INTO the invoice entry (before posting)
    # ------------------------------------------------------------------

    def _post(self, soft=True):
        """
        Before posting vendor bills   → redirect service lines to Intermediate.
        Before posting customer invoices → inject COGS/Intermediate lines
          directly into the invoice's own journal entry so a single entry
          carries both the revenue side and the cost side.
          Analytics are copied from each invoice product line.
        """
        # ── Step 1: Redirect purchase service lines ──────────────────────
        for move in self.filtered(lambda m: m.move_type in _PURCHASE_TYPES):
            move._coa_redirect_service_purchase_lines()

        # ── Step 2: Inject cost lines into sale invoices ─────────────────
        for move in self.filtered(lambda m: m.move_type in _SALE_TYPES):
            move._coa_inject_cost_lines()

        # ── Step 3: Post ──────────────────────────────────────────────────
        return super()._post(soft=soft)

    # ------------------------------------------------------------------
    # button_draft(): remove injected cost lines before reset
    # ------------------------------------------------------------------

    def button_draft(self):
        """Reset to draft first, then remove injected COGS lines.
        Order matters: lines can only be deleted after state = 'draft'."""
        res = super().button_draft()
        for move in self.filtered(lambda m: m.move_type in _SALE_TYPES):
            move._coa_remove_cost_lines()
        return res

    # ------------------------------------------------------------------
    # Purchase: redirect expense account → Intermediate Account
    # ------------------------------------------------------------------

    def _coa_redirect_service_purchase_lines(self):
        self.ensure_one()
        for line in self.invoice_line_ids.filtered(
                lambda l: l.display_type == 'product'):
            product = line.product_id.with_company(self.company_id)
            intermediate = (
                product.product_tmpl_id.coa_service_intermediate_account_id)
            if product and product.type == 'service' and intermediate:
                if line.account_id != intermediate:
                    line.account_id = intermediate
                    _logger.info(
                        "COA: %s – redirected '%s' → Intermediate %s",
                        self.name, product.display_name, intermediate.code)

    # ------------------------------------------------------------------
    # Sale: inject COGS ↔ Intermediate lines into the invoice entry
    # ------------------------------------------------------------------

    def _coa_inject_cost_lines(self):
        """
        Add service-cost lines directly to this invoice's line_ids so they
        become part of the single posted journal entry.

          DR  Cost of Sales   (standard_price × qty)  ← analytic from invoice line
          CR  Intermediate    (standard_price × qty)

        Lines are tagged with _COA_LINE_MARKER in their name so they can be
        found and removed cleanly on reset-to-draft.
        """
        self.ensure_one()

        # Guard: don't inject twice
        if self.line_ids.filtered(
                lambda l: l.name and l.name.startswith(_COA_LINE_MARKER)):
            return

        is_refund      = self.move_type == 'out_refund'
        lines_to_create = []

        for line in self.invoice_line_ids.filtered(
                lambda l: l.display_type == 'product'):
            product      = line.product_id.with_company(self.company_id)
            tmpl         = product.product_tmpl_id
            intermediate = tmpl.coa_service_intermediate_account_id
            cogs         = tmpl.coa_service_cogs_account_id

            if not (product.type == 'service' and intermediate and cogs):
                continue

            cost_amount = product.standard_price * line.quantity
            if not cost_amount:
                continue

            # Direction: invoice → DR COGS / CR Intermediate
            #            refund  → DR Intermediate / CR COGS
            if is_refund:
                debit_acc, credit_acc = intermediate.id, cogs.id
            else:
                debit_acc, credit_acc = cogs.id, intermediate.id

            label    = f"{_COA_LINE_MARKER} {line.name or product.display_name}"
            analytic = line.analytic_distribution  # ← copy analytics

            common = {
                'move_id':               self.id,
                'display_type':          'cogs',
                'name':                  label,
                'partner_id':            self.partner_id.id,
                'currency_id':           self.currency_id.id,
                'company_id':            self.company_id.id,
                'analytic_distribution': analytic,
            }
            lines_to_create += [
                {**common, 'account_id': debit_acc,
                 'debit': cost_amount, 'credit': 0.0},
                {**common, 'account_id': credit_acc,
                 'debit': 0.0,         'credit': cost_amount},
            ]

        if lines_to_create:
            self.env['account.move.line'].with_context(
                check_move_validity=False,
            ).create(lines_to_create)
            _logger.info(
                "COA: injected %d cost line(s) into invoice %s",
                len(lines_to_create), self.name)

    def _coa_remove_cost_lines(self):
        """Remove previously injected cost lines (called on reset-to-draft)."""
        self.ensure_one()
        cost_lines = self.line_ids.filtered(
            lambda l: l.name and l.name.startswith(_COA_LINE_MARKER))
        if cost_lines:
            cost_lines.with_context(check_move_validity=False).unlink()
            _logger.info(
                "COA: removed %d cost line(s) from invoice %s on reset-to-draft",
                len(cost_lines), self.name)
