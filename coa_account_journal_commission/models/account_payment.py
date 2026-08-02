# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import float_round


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # المبلغ قبل الخصم — اليوزر بيكتب فيه
    amount_before_commission = fields.Monetary(
        string='المبلغ قبل خصم العمولة',
        currency_field='currency_id',
        store=True,
    )

    # نسبة العمولة المحسوبة من الـ Journal
    commission_rate = fields.Float(
        string='نسبة العمولة %',
        compute='_compute_commission_info',
        store=True,
        readonly=True,
    )

    # قيمة العمولة بالجنيه
    commission_amount = fields.Monetary(
        string='قيمة العمولة',
        compute='_compute_commission_info',
        store=True,
        readonly=True,
        currency_field='currency_id',
    )

    # هل الـ Journal ده عنده عمولة على نوع الحركة دي
    has_active_commission = fields.Boolean(
        string='عنده عمولة',
        compute='_compute_commission_info',
        store=True,
    )

    @api.depends('journal_id', 'payment_type', 'amount_before_commission', 'amount')
    def _compute_commission_info(self):
        for rec in self:
            journal = rec.journal_id
            rate = 0.0
            active = False

            if journal:
                # سداد من العميل = مبيعات (inbound)
                if rec.payment_type == 'inbound' and journal.sale_has_commission:
                    rate = journal.sale_commission_rate
                    active = True
                # سداد للمورد = مشتريات (outbound)
                elif rec.payment_type == 'outbound' and journal.purchase_has_commission:
                    rate = journal.purchase_commission_rate
                    active = True

            rec.commission_rate = rate
            rec.has_active_commission = active

            # احسب قيمة العمولة من المبلغ قبل الخصم لو موجود
            base = rec.amount_before_commission or rec.amount or 0.0
            rec.commission_amount = float_round(base * rate / 100, precision_digits=2) if rate else 0.0

    @api.onchange('amount_before_commission', 'journal_id', 'payment_type')
    def _onchange_apply_commission(self):
        """لما تكتب المبلغ قبل الخصم — يحسب تلقائي ويحط الصافي في amount"""
        for rec in self:
            if rec.amount_before_commission and rec.commission_rate:
                rate = rec.commission_rate / 100
                net = float_round(
                    rec.amount_before_commission * (1 - rate),
                    precision_digits=2
                )
                rec.amount = net
            elif rec.amount_before_commission and not rec.commission_rate:
                # لو مفيش عمولة — المبلغ بيتنقل عادي
                rec.amount = rec.amount_before_commission
