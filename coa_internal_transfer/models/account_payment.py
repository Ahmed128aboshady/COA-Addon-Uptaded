# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # ------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------
    is_internal_transfer = fields.Boolean(
        string="Internal Transfer",
        readonly=False,
        store=True,
        tracking=True,
        help="Check this box to mark this payment as an internal transfer "
             "between two of your own bank/cash journals.",
    )
    destination_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Destination Journal",
        readonly=False,
        store=True,
        copy=False,
        domain="[('type', 'in', ('bank', 'cash')), ('id', '!=', journal_id), "
               "('company_id', '=', company_id)]",
        check_company=True,
        help="The journal that will receive the transferred amount.",
    )

    # ------------------------------------------------------------------
    # COMPUTE OVERRIDES
    # ------------------------------------------------------------------
    @api.depends('destination_journal_id', 'is_internal_transfer')
    def _compute_destination_account_id(self):
        """
        For internal transfers, the counterpart account is the
        destination journal's liquidity (bank/cash) account.
        This produces a direct Bank A → Bank B entry with no intermediate.
        """
        super()._compute_destination_account_id()
        for pay in self:
            if pay.is_internal_transfer and pay.destination_journal_id:
                pay.destination_account_id = pay.destination_journal_id.default_account_id

    @api.depends('is_internal_transfer', 'journal_id')
    def _compute_outstanding_account_id(self):
        """
        For internal transfers, force the liquidity line to use the
        source journal's default account directly (not the
        outstanding payments/receipts account).
        """
        super()._compute_outstanding_account_id()
        for pay in self:
            if pay.is_internal_transfer and pay.journal_id:
                pay.outstanding_account_id = pay.journal_id.default_account_id

    # ------------------------------------------------------------------
    # ONCHANGE / CONSTRAINTS
    # ------------------------------------------------------------------
    @api.onchange('is_internal_transfer')
    def _onchange_is_internal_transfer(self):
        if self.is_internal_transfer:
            self.payment_type = 'outbound'
            self.partner_id = False
            self.partner_type = 'supplier'
        else:
            self.destination_journal_id = False

    @api.onchange('destination_journal_id')
    def _onchange_destination_journal_id(self):
        if self.destination_journal_id and self.destination_journal_id == self.journal_id:
            self.destination_journal_id = False

    @api.constrains('is_internal_transfer', 'destination_journal_id', 'journal_id')
    def _check_internal_transfer_journals(self):
        for pay in self:
            if pay.is_internal_transfer:
                if not pay.destination_journal_id:
                    raise ValidationError(_(
                        "Please select a Destination Journal for the internal "
                        "transfer on payment %(name)s.",
                        name=pay.display_name,
                    ))
                if pay.destination_journal_id == pay.journal_id:
                    raise ValidationError(_(
                        "The destination journal must be different from the "
                        "source journal (%(name)s).",
                        name=pay.display_name,
                    ))

    # ------------------------------------------------------------------
    # LABEL OVERRIDE
    # ------------------------------------------------------------------
    def _get_aml_default_display_name_list(self):
        self.ensure_one()
        if self.is_internal_transfer and self.destination_journal_id:
            label = _("Transfer to %(journal)s",
                      journal=self.destination_journal_id.name)
            return [('label', label)]
        return super()._get_aml_default_display_name_list()

    # ------------------------------------------------------------------
    # ACTION POST — no paired payment needed
    # ------------------------------------------------------------------
    def action_post(self):
        """
        Validate internal-transfer constraints before posting.
        No paired payment is created: the single payment already posts a
        direct journal entry  Dr. Destination Bank / Cr. Source Bank.
        """
        transfers = self.filtered(
            lambda p: p.is_internal_transfer and not p.paired_internal_transfer_payment_id
        )
        transfers._check_internal_transfer_journals()
        return super().action_post()

    # ------------------------------------------------------------------
    # SMART BUTTON (kept for compatibility if paired_id is ever set)
    # ------------------------------------------------------------------
    def button_open_paired_internal_transfer_payment(self):
        self.ensure_one()
        return {
            'name': _("Paired Internal Transfer"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'res_id': self.paired_internal_transfer_payment_id.id,
        }
