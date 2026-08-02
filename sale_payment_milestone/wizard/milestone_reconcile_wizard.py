# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MilestoneReconcileWizard(models.TransientModel):
    """
    Wizard لربط دفعة محاسبية موجودة (account.payment) بمرحلة سداد.
    يعمل كـ manual reconciliation من شاشة المبيعات.
    """
    _name = 'milestone.reconcile.wizard'
    _description = 'ربط دفعة بمرحلة'

    order_id = fields.Many2one(
        'sale.order',
        string='أوردر البيع',
        required=True,
        readonly=True,
    )
    milestone_id = fields.Many2one(
        'sale.payment.milestone',
        string='المرحلة',
        required=True,
        domain="[('order_id', '=', order_id)]",
    )
    milestone_amount = fields.Monetary(
        string='المبلغ المستحق للمرحلة',
        related='milestone_id.amount',
        currency_field='currency_id',
    )
    milestone_paid = fields.Monetary(
        string='المدفوع مسبقاً',
        related='milestone_id.paid_amount',
        currency_field='currency_id',
    )
    milestone_remaining = fields.Monetary(
        string='المتبقي للمرحلة',
        related='milestone_id.remaining_amount',
        currency_field='currency_id',
    )

    # اختيار السند من المحاسبة
    partner_id = fields.Many2one(
        related='order_id.partner_id',
        string='العميل',
    )
    available_payment_ids = fields.Many2many(
        'account.payment',
        string='الدفعات المتاحة',
        compute='_compute_available_payments',
    )
    payment_id = fields.Many2one(
        'account.payment',
        string='سند القبض',
        required=True,
        domain="[('id', 'in', available_payment_ids)]",
    )
    payment_amount = fields.Monetary(
        string='قيمة السند',
        related='payment_id.amount',
        currency_field='currency_id',
    )
    payment_available = fields.Monetary(
        string='المتاح في السند',
        related='payment_id.milestone_available_amount',
        currency_field='currency_id',
    )
    payment_date = fields.Date(
        related='payment_id.date',
        string='تاريخ السند',
    )

    amount = fields.Monetary(
        string='المبلغ المُرحَّل',
        currency_field='currency_id',
        required=True,
    )
    currency_id = fields.Many2one(
        related='order_id.currency_id',
    )
    note = fields.Char(string='ملاحظة')

    def _compute_available_payments(self):
        for rec in self:
            domain = [
                ('payment_type', '=', 'inbound'),
                ('state', 'in', ['in_process', 'paid']),
            ]
            # فلتر بعميل الأوردر إذا كان محدداً
            if rec.order_id.partner_id:
                domain.append(
                    ('partner_id', 'child_of', rec.order_id.partner_id.id)
                )
            payments = self.env['account.payment'].search(domain)
            rec.available_payment_ids = [(6, 0, payments.ids)]

    @api.onchange('milestone_id')
    def _onchange_milestone(self):
        if self.milestone_id:
            self.amount = self.milestone_id.remaining_amount

    @api.onchange('payment_id')
    def _onchange_payment(self):
        if self.payment_id and self.milestone_id:
            # اقترح أقل القيمتين: المتبقي للمرحلة أو المتاح في السند
            available = self.payment_id.milestone_available_amount
            remaining = self.milestone_id.remaining_amount
            self.amount = min(available, remaining)

    def action_reconcile(self):
        self.ensure_one()
        if self.amount <= 0:
            raise UserError(_('المبلغ يجب أن يكون أكبر من صفر'))
        if self.amount > self.payment_id.milestone_available_amount + 0.001:
            raise UserError(_(
                'المبلغ المُرحَّل (%(a)s) يتجاوز المتاح في السند (%(b)s)',
                a=f'{self.amount:,.2f}',
                b=f'{self.payment_id.milestone_available_amount:,.2f}',
            ))
        if self.amount > self.milestone_id.remaining_amount + 0.001:
            raise UserError(_(
                'المبلغ المُرحَّل (%(a)s) يتجاوز المتبقي للمرحلة (%(b)s)',
                a=f'{self.amount:,.2f}',
                b=f'{self.milestone_id.remaining_amount:,.2f}',
            ))

        line = self.env['sale.milestone.payment.line'].create({
            'milestone_id': self.milestone_id.id,
            'payment_id': self.payment_id.id,
            'amount': self.amount,
            'note': self.note,
        })

        # رسالة في chatter الأوردر
        self.order_id.message_post(
            body=_(
                '✅ تم ترحيل <b>%(amount)s %(currency)s</b> من سند '
                '<a href="/odoo/accounting/payments/%(pid)s">%(pname)s</a> '
                'على مرحلة <b>%(milestone)s</b>',
                amount=f'{self.amount:,.2f}',
                currency=self.currency_id.symbol or '',
                pid=self.payment_id.id,
                pname=self.payment_id.name,
                milestone=self.milestone_id.name,
            ),
            message_type='notification',
            subtype_xmlid='mail.mt_note',
        )
        return {'type': 'ir.actions.act_window_close'}

    def action_reconcile_and_new(self):
        """رحِّل وافتح wizard جديد على نفس الأوردر"""
        self.action_reconcile()
        return {
            'type': 'ir.actions.act_window',
            'name': _('ربط دفعة'),
            'res_model': 'milestone.reconcile.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.order_id.id,
            },
        }
