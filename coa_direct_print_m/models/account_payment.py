# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models
from odoo.odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # ------------------------------------------------------------------
    # Computed: partner balance before / after this payment
    # ------------------------------------------------------------------

    coa_balance_before = fields.Monetary(
        string='الرصيد قبل الدفعة / Balance Before',
        compute='_compute_coa_balances',
        currency_field='currency_id',
    )
    coa_balance_after = fields.Monetary(
        string='الرصيد بعد الدفعة / Balance After',
        compute='_compute_coa_balances',
        currency_field='currency_id',
    )

    @api.depends(
        'partner_id', 'amount', 'payment_type',
        'state', 'move_id', 'company_id',
    )
    def _compute_coa_balances(self):
        AML = self.env['account.move.line']

        for payment in self:
            partner = payment.partner_id.commercial_partner_id
            company = payment.company_id

            if not partner or not company or payment.payment_type == 'transfer':
                payment.coa_balance_before = 0.0
                payment.coa_balance_after = 0.0
                continue

            # Account type to look at
            if payment.payment_type == 'inbound':
                acc_types = ['asset_receivable']
            else:
                acc_types = ['liability_payable']

            # All posted move lines for this partner on the relevant account
            domain = [
                ('partner_id', 'child_of', partner.id),
                ('account_id.account_type', 'in', acc_types),
                ('parent_state', '=', 'posted'),
                ('company_id', '=', company.id),
            ]
            all_lines = AML.search(domain)
            current_balance = sum(all_lines.mapped('balance'))

            if payment.state in ('in_process', 'paid') and payment.move_id:
                # Payment is already posted → current balance INCLUDES this payment.
                # Remove its effect to get the balance BEFORE.
                pay_lines = all_lines.filtered(
                    lambda l, m=payment.move_id: l.move_id == m)
                pay_effect = sum(pay_lines.mapped('balance'))
                balance_after  = current_balance
                balance_before = current_balance - pay_effect
            else:
                # Draft/cancel → current balance does NOT yet include this payment.
                balance_before = current_balance
                if payment.payment_type == 'inbound':
                    # Customer pays → credits AR → reduces positive balance
                    balance_after = current_balance - payment.amount
                else:
                    # We pay vendor → debits AP → increases (less negative) balance
                    balance_after = current_balance + payment.amount

            payment.coa_balance_before = balance_before
            payment.coa_balance_after  = balance_after

    # ------------------------------------------------------------------
    # Direct print action (opens the COA print page)
    # ------------------------------------------------------------------

    def action_coa_print_receipt(self):
        """Print payment receipt using Odoo standard report action (no popup)."""
        self.ensure_one()
        return self.env.ref(
            'coa_direct_print_m.action_report_payment_receipt'
        ).report_action(self)

    def action_coa_print_statement(self):
        """Print partner statement using Odoo standard report action (no popup)."""
        self.ensure_one()
        partner = self.partner_id.commercial_partner_id
        if not partner:
            raise UserError(_("This payment has no partner set."))
        return self.env.ref(
            'coa_direct_print_m.action_report_partner_statement'
        ).report_action(partner)
