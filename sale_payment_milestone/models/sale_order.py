# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_milestone_ids = fields.One2many(
        'sale.payment.milestone',
        'order_id',
        string='جدول الدفعات',
    )
    
    # === الحقول المتسجلة (store=True) ===
    milestone_total_pct = fields.Float(
        string='إجمالي النسب %',
        compute='_compute_milestone_summary_stored',
        store=True,
    )
    milestone_paid_amount = fields.Monetary(
        string='إجمالي المدفوع',
        compute='_compute_milestone_summary_stored',
        store=True,
    )
    milestone_remaining_amount = fields.Monetary(
        string='إجمالي المتبقي',
        compute='_compute_milestone_summary_stored',
        store=True,
    )
    milestone_paid_pct = fields.Float(
        string='% السداد الكلي',
        compute='_compute_milestone_summary_stored',
        store=True,
    )
    milestone_count = fields.Integer(
        string='عدد المراحل',
        compute='_compute_milestone_summary_stored',
        store=True,
    )
    
    # === الحقول الغير متسجلة (store=False) ===
    milestone_warning = fields.Char(
        string='تنبيه',
        compute='_compute_milestone_summary_non_stored',
    )
    
    milestone_payment_count = fields.Integer(
        string='عدد سندات القبض',
        compute='_compute_milestone_payment_count',
    )

    def _compute_milestone_payment_count(self):
        for order in self:
            order.milestone_payment_count = len(
                order.payment_milestone_ids.payment_line_ids.mapped('payment_id')
            )

    @api.depends(
        'payment_milestone_ids',
        'payment_milestone_ids.percentage',
        'payment_milestone_ids.paid_amount',
        'amount_total',
    )
    def _compute_milestone_summary_stored(self):
        for order in self:
            milestones = order.payment_milestone_ids
            order.milestone_count = len(milestones)
            order.milestone_total_pct = sum(milestones.mapped('percentage'))
            order.milestone_paid_amount = sum(milestones.mapped('paid_amount'))
            order.milestone_remaining_amount = (
                order.amount_total - order.milestone_paid_amount
            )
            if order.amount_total > 0:
                order.milestone_paid_pct = (
                    order.milestone_paid_amount / order.amount_total
                ) * 100.0
            else:
                order.milestone_paid_pct = 0.0

    @api.depends('payment_milestone_ids', 'milestone_total_pct')
    def _compute_milestone_summary_non_stored(self):
        for order in self:
            milestones = order.payment_milestone_ids
            total_pct = order.milestone_total_pct
            if milestones and abs(total_pct - 100.0) > 0.01:
                order.milestone_warning = _(
                    'تحذير: مجموع النسب %(pct).1f%% وليس 100%%',
                    pct=total_pct,
                )
            else:
                order.milestone_warning = False

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            triggered = order.payment_milestone_ids.filtered(
                lambda m: m.trigger == 'sale_confirm'
            )
            if triggered:
                order._notify_milestone_due(triggered)
        return res

    def _notify_milestone_due(self, milestones):
        """إرسال إشعار داخلي للمبيعات عند استحقاق دفعة"""
        for milestone in milestones:
            self.message_post(
                body=_(
                    '💰 <b>دفعة مستحقة:</b> %(name)s — %(amount)s '
                    '(%(pct)s%% من إجمالي الأوردر)',
                    name=milestone.name,
                    amount=f'{milestone.amount:,.2f} {milestone.currency_id.symbol}',
                    pct=milestone.percentage,
                ),
                message_type='notification',
                subtype_xmlid='mail.mt_note',
            )

    def action_view_milestone_payments(self):
        """فتح قائمة بكل الدفعات المرتبطة بهذا الأوردر"""
        self.ensure_one()
        payment_ids = self.payment_milestone_ids.payment_line_ids.mapped(
            'payment_id'
        ).ids
        return {
            'type': 'ir.actions.act_window',
            'name': _('مدفوعات — %s') % self.name,
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', payment_ids)],
        }

    # ─── Triggers من خارج الأدون (Production / Delivery) ───────────────────

    def _trigger_milestone(self, trigger_key):
        """
        يُستدعى من أدوانات أخرى (mrp, stock) لتحريك المراحل.
        مثال: order._trigger_milestone('production_start')
        """
        triggered = self.payment_milestone_ids.filtered(
            lambda m: m.trigger == trigger_key and m.state == 'pending'
        )
        if triggered:
            self._notify_milestone_due(triggered)
        return triggered