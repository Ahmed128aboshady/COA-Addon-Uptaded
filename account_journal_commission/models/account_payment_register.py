# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import float_round


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    amount_before_commission = fields.Monetary(
        string='المبلغ قبل خصم العمولة',
        currency_field='currency_id',
    )
    commission_rate = fields.Float(
        string='نسبة العمولة %',
        compute='_compute_register_commission_info',
        store=True,
        readonly=True,
    )
    commission_amount = fields.Monetary(
        string='قيمة العمولة',
        compute='_compute_register_commission_info',
        store=True,
        readonly=True,
        currency_field='currency_id',
    )
    has_active_commission = fields.Boolean(
        string='عنده عمولة',
        compute='_compute_register_commission_info',
        store=True,
    )

    @api.depends('journal_id', 'payment_type', 'amount_before_commission', 'amount')
    def _compute_register_commission_info(self):
        for rec in self:
            journal = rec.journal_id
            rate = 0.0
            active = False

            if journal:
                if rec.payment_type == 'inbound' and journal.sale_has_commission:
                    rate = journal.sale_commission_rate
                    active = True
                elif rec.payment_type == 'outbound' and journal.purchase_has_commission:
                    rate = journal.purchase_commission_rate
                    active = True

            rec.commission_rate = rate
            rec.has_active_commission = active

            base = rec.amount_before_commission or rec.amount or 0.0
            rec.commission_amount = float_round(base * rate / 100, precision_digits=2) if rate else 0.0

    @api.onchange('amount_before_commission', 'journal_id', 'payment_type')
    def _onchange_register_apply_commission(self):
        for rec in self:
            if rec.amount_before_commission and rec.commission_rate:
                net = float_round(
                    rec.amount_before_commission * (1 - rec.commission_rate / 100),
                    precision_digits=2,
                )
                rec.amount = net
            elif rec.amount_before_commission and not rec.commission_rate:
                rec.amount = rec.amount_before_commission

    def _create_payment_vals_from_wizard(self, batch_result):
        """أضيف بيانات العمولة على الـ payment اللي بيتعمل من الـ wizard"""
        vals = super()._create_payment_vals_from_wizard(batch_result)
        if self.has_active_commission:
            vals['amount_before_commission'] = self.amount_before_commission
        return vals
