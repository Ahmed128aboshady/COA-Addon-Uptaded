# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SalePaymentMilestone(models.Model):
    _name = 'sale.payment.milestone'
    _description = 'مرحلة سداد على أوردر البيع'
    _order = 'sequence, id'

    sequence = fields.Integer(string='الترتيب', default=10)
    order_id = fields.Many2one(
        'sale.order',
        string='أوردر البيع',
        required=True,
        ondelete='cascade',
        index=True,
    )
    name = fields.Char(string='اسم المرحلة', required=True)
    trigger = fields.Selection([
        ('manual', 'يدوي'),
        ('sale_confirm', 'تأكيد الأوردر'),
        ('production_start', 'بداية التصنيع'),
        ('production_done', 'انتهاء التصنيع'),
        ('delivery', 'التسليم'),
    ], string='عند', default='manual', required=True)
    percentage = fields.Float(
        string='النسبة %',
        digits=(5, 2),
        required=True,
    )
    amount = fields.Monetary(
        string='المبلغ المستحق',
        currency_field='currency_id',
        compute='_compute_amount',
        store=True,
    )
    currency_id = fields.Many2one(
        related='order_id.currency_id',
        store=True,
    )
    company_id = fields.Many2one(
        related='order_id.company_id',
        store=True,
    )
    # الدفعات المرتبطة بهذه المرحلة
    payment_line_ids = fields.One2many(
        'sale.milestone.payment.line',
        'milestone_id',
        string='الدفعات المرتبطة',
    )
    paid_amount = fields.Monetary(
        string='المدفوع',
        currency_field='currency_id',
        compute='_compute_paid',
        store=True,
    )
    remaining_amount = fields.Monetary(
        string='المتبقي',
        currency_field='currency_id',
        compute='_compute_paid',
        store=True,
    )
    paid_percentage = fields.Float(
        string='% المدفوع',
        compute='_compute_paid',
        store=True,
    )
    state = fields.Selection([
        ('pending', 'معلق'),
        ('partial', 'جزئي'),
        ('paid', 'مكتمل'),
    ], string='الحالة', compute='_compute_paid', store=True)

    note = fields.Text(string='ملاحظات')

    @api.depends('percentage', 'order_id.amount_total')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.order_id.amount_total * rec.percentage / 100.0

    @api.depends('payment_line_ids.amount', 'amount')
    def _compute_paid(self):
        for rec in self:
            paid = sum(rec.payment_line_ids.mapped('amount'))
            rec.paid_amount = paid
            rec.remaining_amount = rec.amount - paid
            if rec.amount > 0:
                rec.paid_percentage = (paid / rec.amount) * 100.0
            else:
                rec.paid_percentage = 0.0
            if paid <= 0:
                rec.state = 'pending'
            elif paid >= rec.amount:
                rec.state = 'paid'
            else:
                rec.state = 'partial'

    @api.constrains('percentage')
    def _check_percentage(self):
        for rec in self:
            if rec.percentage < 0 or rec.percentage > 100:
                raise ValidationError(_('النسبة يجب أن تكون بين 0 و 100'))

    def action_open_reconcile_wizard(self):
        """فتح wizard لربط دفعة محاسبية بهذه المرحلة"""
        self.ensure_one()
        # جلب IDs الدفعات المتاحة مفلترةً بعميل الأوردر
        domain = [
            ('payment_type', '=', 'inbound'),
            ('state', 'in', ['in_process', 'paid']),
        ]
        if self.order_id.partner_id:
            domain.append(('partner_id', 'child_of', self.order_id.partner_id.id))
        available_payment_ids = self.env['account.payment'].search(domain).ids
        return {
            'type': 'ir.actions.act_window',
            'name': _('ربط دفعة — %s') % self.name,
            'res_model': 'milestone.reconcile.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_milestone_id': self.id,
                'default_order_id': self.order_id.id,
                'default_amount': self.remaining_amount,
                'available_payment_ids': available_payment_ids,
            },
        }


class SaleMilestonePaymentLine(models.Model):
    """
    سطر الربط بين المرحلة والدفعة المحاسبية الفعلية.
    يعمل كـ reconciliation line بدون الحاجة لفاتورة.
    """
    _name = 'sale.milestone.payment.line'
    _description = 'سطر ربط دفعة بمرحلة'

    milestone_id = fields.Many2one(
        'sale.payment.milestone',
        required=True,
        ondelete='cascade',
        index=True,
    )
    order_id = fields.Many2one(
        related='milestone_id.order_id',
        store=True,
        index=True,
    )
    payment_id = fields.Many2one(
        'account.payment',
        string='سند القبض',
        required=True,
        domain=[('payment_type', '=', 'inbound'), ('state', 'in', ['in_process', 'paid'])],
    )
    payment_date = fields.Date(
        related='payment_id.date',
        string='تاريخ الدفعة',
        store=True,
    )
    payment_ref = fields.Char(
        related='payment_id.name',
        string='مرجع السند',
        store=True,
    )
    amount = fields.Monetary(
        string='المبلغ المُرحَّل',
        currency_field='currency_id',
        required=True,
    )
    currency_id = fields.Many2one(
        related='milestone_id.currency_id',
        store=True,
    )
    journal_id = fields.Many2one(
        related='payment_id.journal_id',
        string='الدفتر',
        store=True,
    )
    note = fields.Char(string='ملاحظة')

    @api.constrains('amount', 'payment_id')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_('المبلغ يجب أن يكون أكبر من صفر'))
            # التحقق أن مجموع ما رُحِّل من هذا السند لا يتجاوز قيمته
            total_reconciled = sum(
                self.search([
                    ('payment_id', '=', rec.payment_id.id),
                    ('id', '!=', rec.id),
                ]).mapped('amount')
            )
            if total_reconciled + rec.amount > rec.payment_id.amount:
                raise ValidationError(_(
                    'المبلغ المُرحَّل (%(reconciled)s) يتجاوز قيمة سند القبض (%(payment)s)',
                    reconciled=total_reconciled + rec.amount,
                    payment=rec.payment_id.amount,
                ))
