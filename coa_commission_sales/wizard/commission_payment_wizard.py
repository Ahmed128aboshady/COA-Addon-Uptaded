# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CommissionPaymentWizard(models.TransientModel):
    _name = 'commission.payment.wizard'
    _description = 'تسجيل دفعة عمولة'

    commission_id = fields.Many2one(
        'commission.line',
        string='سجل العمولة',
        required=True,
        readonly=True,
    )
    salesperson_name = fields.Char(
        related='commission_id.salesperson_id.name',
        string='المندوب',
        readonly=True,
    )
    total_commission = fields.Monetary(
        related='commission_id.total_commission',
        string='إجمالي العمولة',
        readonly=True,
    )
    amount_paid = fields.Monetary(
        related='commission_id.amount_paid',
        string='المدفوع سابقاً',
        readonly=True,
    )
    amount_residual = fields.Monetary(
        related='commission_id.amount_residual',
        string='المتبقي',
        readonly=True,
    )
    currency_id = fields.Many2one(
        related='commission_id.currency_id',
        readonly=True,
    )

    # ─── حقول الدفعة ────────────────────────────────────────────────────────
    amount = fields.Monetary(string='المبلغ المدفوع', required=True)
    date = fields.Date(
        string='تاريخ الدفع',
        required=True,
        default=fields.Date.today,
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='حساب الدفع (بنك / صندوق)',
        required=True,
        domain=[('type', 'in', ['bank', 'cash'])],
    )
    memo = fields.Char(
        string='البيان',
        default=lambda self: _('دفعة عمولة'),
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        commission_id = self.env.context.get('active_id')
        if commission_id:
            commission = self.env['commission.line'].browse(commission_id)
            res['commission_id'] = commission.id
            res['amount'] = commission.amount_residual
            # يستخدم أول بنك/صندوق متاح كافتراضي
            default_journal = self.env['account.journal'].search(
                [('type', 'in', ['bank', 'cash']), ('company_id', '=', self.env.company.id)],
                limit=1,
            )
            if default_journal:
                res['journal_id'] = default_journal.id
        return res

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_('يجب أن يكون المبلغ أكبر من الصفر.'))
            if rec.amount > rec.commission_id.amount_residual + 0.001:
                raise ValidationError(_(
                    'المبلغ المدخل (%(amount)s) أكبر من المتبقي (%(residual)s).',
                    amount=rec.amount,
                    residual=rec.commission_id.amount_residual,
                ))

    def action_pay(self):
        self.ensure_one()
        commission = self.commission_id
        company = self.env.company

        if not company.commission_credit_account_id:
            raise UserError(_(
                'لم يتم تحديد حساب الدائن (حساب العمولات المستحقة).\n'
                'الرجاء الضبط من: المبيعات ← الإعدادات ← العمولات.'
            ))

        # ── الحساب الدائن للتسوية: نفس الحساب المستخدم في قيد الاستحقاق ──
        payable_account = company.commission_credit_account_id

        # ── حساب البنك/الصندوق من اليومية المختارة ──
        bank_account = (
            self.journal_id.default_account_id
            or self.journal_id.payment_credit_account_id
        )
        if not bank_account:
            raise UserError(_(
                'اليومية "%s" لا تحتوي على حساب افتراضي.\n'
                'يرجى تحديد الحساب الافتراضي لليومية.'
            ) % self.journal_id.name)

        label = self.memo or ('دفعة عمولة - %s' % commission.salesperson_id.name)

        # ── إنشاء القيد المحاسبي ──
        #  Dr: حساب العمولات المستحقة (payable) ← تسوية الاستحقاق
        #  Cr: بنك / صندوق
        move_vals = {
            'move_type': 'entry',
            'journal_id': self.journal_id.id,
            'date': self.date,
            'ref': '%s - %s' % (commission.name, label),
            'line_ids': [
                (0, 0, {
                    'name': label,
                    'account_id': payable_account.id,
                    'debit': self.amount,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': label,
                    'account_id': bank_account.id,
                    'debit': 0.0,
                    'credit': self.amount,
                }),
            ],
        }
        move = self.env['account.move'].sudo().create(move_vals)
        move.sudo().action_post()

        # ── إنشاء سجل الدفعة ──
        seq = self.env['ir.sequence'].next_by_code('commission.payment') or '/'
        payment = self.env['commission.payment'].create({
            'name': seq,
            'commission_id': commission.id,
            'date': self.date,
            'amount': self.amount,
            'journal_id': self.journal_id.id,
            'memo': self.memo,
            'move_id': move.id,
        })

        # ── رسالة في الـ chatter ──
        commission.message_post(body=_(
            'تم تسجيل دفعة بمبلغ <strong>%(amount)s %(currency)s</strong> '
            'بتاريخ %(date)s — %(journal)s '
            '(<a href="#" data-oe-model="account.move" data-oe-id="%(move_id)d">%(move_name)s</a>).',
            amount=self.amount,
            currency=commission.currency_id.name,
            date=self.date,
            journal=self.journal_id.name,
            move_id=move.id,
            move_name=move.name,
        ))

        # تحديث حالة العمولة بناءً على المدفوع
        commission._update_payment_state()

        return {'type': 'ir.actions.act_window_close'}
