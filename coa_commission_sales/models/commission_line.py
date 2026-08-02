# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import defaultdict


class CommissionLine(models.Model):
    _name = 'commission.line'
    _description = 'سطر العمولة'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_from desc, salesperson_id'

    name = fields.Char(string='المرجع', readonly=True, copy=False, default='/')
    state = fields.Selection(
        [
            ('draft', 'مسودة'),
            ('confirmed', 'مؤكد'),
            ('partial', 'مدفوع جزئياً'),
            ('paid', 'مدفوع بالكامل'),
        ],
        default='draft',
        string='الحالة',
        tracking=True,
    )

    date_from = fields.Date(string='من تاريخ', required=True)
    date_to = fields.Date(string='إلى تاريخ', required=True)
    salesperson_id = fields.Many2one(
        'res.users',
        string='المندوب',
        required=True,
        default=lambda self: self.env.user,
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id,
    )

    line_ids = fields.One2many(
        'commission.line.detail',
        'commission_id',
        string='التفاصيل',
    )
    payment_ids = fields.One2many(
        'commission.payment',
        'commission_id',
        string='الدفعات',
        readonly=True,
    )
    amount_paid = fields.Monetary(
        string='المدفوع',
        compute='_compute_payment_amounts',
        store=True,
    )
    amount_residual = fields.Monetary(
        string='المتبقي',
        compute='_compute_payment_amounts',
        store=True,
    )

    total_invoiced = fields.Monetary(
        string='إجمالي المبيعات',
        compute='_compute_totals',
        store=True,
    )
    total_refunded = fields.Monetary(
        string='إجمالي المرتجعات',
        compute='_compute_totals',
        store=True,
    )
    total_net_sales = fields.Monetary(
        string='صافي المبيعات',
        compute='_compute_totals',
        store=True,
    )
    total_commission = fields.Monetary(
        string='إجمالي العمولة',
        compute='_compute_totals',
        store=True,
    )

    # ── حقول قيد اليومية ────────────────────────────────────────────────────
    # اليومية والحسابات تأتي من إعدادات الشركة مباشرةً (related — للعرض فقط)
    journal_id = fields.Many2one(
        related='company_id.commission_journal_id',
        string='اليومية',
        readonly=True,
        store=False,
    )
    debit_account_id = fields.Many2one(
        related='company_id.commission_debit_account_id',
        string='حساب المدين',
        readonly=True,
        store=False,
    )
    credit_account_id = fields.Many2one(
        related='company_id.commission_credit_account_id',
        string='حساب الدائن',
        readonly=True,
        store=False,
    )
    company_id = fields.Many2one(
        'res.company',
        string='الشركة',
        required=True,
        default=lambda self: self.env.company,
    )
    move_id = fields.Many2one(
        'account.move',
        string='قيد اليومية',
        readonly=True,
        copy=False,
    )
    move_state = fields.Selection(
        related='move_id.state',
        string='حالة القيد',
        readonly=True,
    )

    # ── الحسابات ─────────────────────────────────────────────────────────────
    @api.depends('payment_ids.amount')
    def _compute_payment_amounts(self):
        for rec in self:
            paid = sum(rec.payment_ids.mapped('amount'))
            rec.amount_paid = paid
            rec.amount_residual = max(0.0, rec.total_commission - paid)

    @api.depends('line_ids.invoiced_amount', 'line_ids.refunded_amount',
                 'line_ids.net_sales', 'line_ids.commission_amount')
    def _compute_totals(self):
        for rec in self:
            rec.total_invoiced = sum(rec.line_ids.mapped('invoiced_amount'))
            rec.total_refunded = sum(rec.line_ids.mapped('refunded_amount'))
            rec.total_net_sales = sum(rec.line_ids.mapped('net_sales'))
            rec.total_commission = sum(rec.line_ids.mapped('commission_amount'))

    def action_compute_commission(self):
        """الحساب الرئيسي: يجلب الفواتير ويحسب العمولة"""
        self.ensure_one()
        if not self.date_from or not self.date_to:
            raise UserError(_('يرجى تحديد الفترة الزمنية أولاً.'))

        self.line_ids.unlink()

        rates = self.env['commission.rate'].search([('active', '=', True)])
        if not rates:
            raise UserError(_('لا توجد نسب عمولة محددة. يرجى الإعداد من قائمة الإعدادات.'))

        tag_rate_map = {r.customer_tag_id.id: r for r in rates}
        tag_ids = list(tag_rate_map.keys())

        # جلب الفواتير المؤكدة في الفترة للمندوب المحدد
        invoices = self.env['account.move'].search([
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('invoice_user_id', '=', self.salesperson_id.id),
        ])

        if not invoices:
            raise UserError(_('لا توجد فواتير مؤكدة للمندوب في هذه الفترة.'))

        # تجميع المبيعات والمرتجعات بشكل منفصل حسب التاج
        tag_invoiced = defaultdict(float)   # مبيعات (فواتير)
        tag_refunded = defaultdict(float)   # مرتجعات (إشعارات دائنة)

        for inv in invoices:
            partner_tags = inv.partner_id.category_id.ids
            matched_tags = set(partner_tags) & set(tag_ids)
            if not matched_tags:
                continue

            amount = inv.amount_untaxed  # دائماً موجب

            for tag_id in matched_tags:
                if inv.move_type == 'out_invoice':
                    tag_invoiced[tag_id] += amount
                else:  # out_refund
                    tag_refunded[tag_id] += amount

        detail_vals = []

        # ── فواتير بعملاء لديهم تاجات مربوطة بنسب عمولة ──
        tagged_tags = set(tag_invoiced) | set(tag_refunded)
        for tag_id in tagged_tags:
            invoiced = tag_invoiced.get(tag_id, 0.0)
            refunded = tag_refunded.get(tag_id, 0.0)
            net_sales = invoiced - refunded
            rate_rec = tag_rate_map[tag_id]
            commission_amount = rate_rec.compute_commission(net_sales)
            detail_vals.append({
                'commission_id': self.id,
                'customer_tag_id': tag_id,
                'commission_rate_id': rate_rec.id,
                'rate_percent': rate_rec.commission_rate,
                'invoiced_amount': invoiced,
                'refunded_amount': refunded,
                'net_sales': net_sales,
                'commission_amount': commission_amount,
            })

        # ── فواتير بعملاء بدون تاج مربوط → UNKNOWN TAG / عمولة صفر ──
        untagged_invoiced = 0.0
        untagged_refunded = 0.0
        for inv in invoices:
            partner_tags = inv.partner_id.category_id.ids
            matched = set(partner_tags) & set(tag_ids)
            if not matched:
                amount = inv.amount_untaxed
                if inv.move_type == 'out_invoice':
                    untagged_invoiced += amount
                else:
                    untagged_refunded += amount

        if untagged_invoiced or untagged_refunded:
            detail_vals.append({
                'commission_id': self.id,
                'customer_tag_id': False,   # لا يوجد تاج
                'commission_rate_id': False,
                'rate_percent': 0.0,
                'invoiced_amount': untagged_invoiced,
                'refunded_amount': untagged_refunded,
                'net_sales': untagged_invoiced - untagged_refunded,
                'commission_amount': 0.0,
            })

        if not detail_vals:
            raise UserError(_('لا توجد فواتير مؤكدة للمندوب في هذه الفترة.'))

        self.env['commission.line.detail'].create(detail_vals)

    # ── سير العمل ────────────────────────────────────────────────────────────
    def action_confirm(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError(_('يرجى حساب العمولة أولاً قبل التأكيد.'))
            seq = self.env['ir.sequence'].next_by_code('commission.line') or '/'
            rec.write({'state': 'confirmed', 'name': seq})

    def action_register_payment(self):
        """فتح wizard تسجيل الدفعة."""
        self.ensure_one()
        if self.amount_residual <= 0:
            raise UserError(_('لا يوجد مبلغ متبقي لهذه العمولة.'))
        return {
            'type': 'ir.actions.act_window',
            'name': 'تسجيل دفعة',
            'res_model': 'commission.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    def _update_payment_state(self):
        """يُستدعى من wizard الدفع لتحديث حالة العمولة."""
        for rec in self:
            if rec.amount_residual <= 0.001 and rec.amount_paid > 0:
                rec.state = 'paid'
            elif rec.amount_paid > 0:
                rec.state = 'partial'

    def action_mark_paid(self):
        self.write({'state': 'paid'})

    def action_reset_draft(self):
        self.write({'state': 'draft', 'payment_ids': [(5, 0, 0)]})

    def action_print_report(self):
        return self.env.ref('commission_sales.action_commission_report').report_action(self)

    # ── قيد اليومية ──────────────────────────────────────────────────────────
    def action_create_journal_entry(self):
        """إنشاء قيد استحقاق للعمولة — الحسابات من إعدادات الشركة."""
        self.ensure_one()
        company = self.env.company

        if not self.total_commission:
            raise UserError(_('مبلغ العمولة صفر. يرجى حساب العمولة أولاً.'))
        if not company.commission_journal_id:
            raise UserError(_(
                'لم يتم تحديد يومية العمولات.\n'
                'الرجاء الضبط من: المبيعات ← الإعدادات ← العمولات.'
            ))
        if not company.commission_debit_account_id:
            raise UserError(_(
                'لم يتم تحديد حساب المدين.\n'
                'الرجاء الضبط من: المبيعات ← الإعدادات ← العمولات.'
            ))
        if not company.commission_credit_account_id:
            raise UserError(_(
                'لم يتم تحديد حساب الدائن.\n'
                'الرجاء الضبط من: المبيعات ← الإعدادات ← العمولات.'
            ))
        if self.move_id:
            raise UserError(_('يوجد قيد محاسبي مسجل بالفعل لهذا السجل.'))

        amount = self.total_commission
        label = 'عمولة - %s (%s إلى %s)' % (
            self.salesperson_id.name,
            self.date_from,
            self.date_to,
        )

        move_vals = {
            'move_type': 'entry',
            'journal_id': company.commission_journal_id.id,
            'date': self.date_to,
            'ref': self.name,
            'line_ids': [
                (0, 0, {
                    'name': label,
                    'account_id': company.commission_debit_account_id.id,
                    'debit': amount,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': label,
                    'account_id': company.commission_credit_account_id.id,
                    'debit': 0.0,
                    'credit': amount,
                }),
            ],
        }

        move = self.env['account.move'].sudo().create(move_vals)
        self.move_id = move

        self.message_post(body=_(
            'تم إنشاء قيد اليومية <a href="#" data-oe-model="account.move" data-oe-id="%d">%s</a>.'
        ) % (move.id, move.name))

        return {
            'type': 'ir.actions.act_window',
            'name': 'قيد اليومية',
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
        }

    def action_view_journal_entry(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'قيد اليومية',
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'view_mode': 'form',
        }


class CommissionLineDetail(models.Model):
    _name = 'commission.line.detail'
    _description = 'تفاصيل سطر العمولة'
    _order = 'customer_tag_id'

    commission_id = fields.Many2one('commission.line', ondelete='cascade')
    customer_tag_id = fields.Many2one('res.partner.category', string='تاج العميل', readonly=True,
                                      required=False)
    commission_rate_id = fields.Many2one('commission.rate', string='نسبة العمولة', readonly=True)
    rate_percent = fields.Float(string='النسبة %', readonly=True, digits=(5, 4))
    currency_id = fields.Many2one(related='commission_id.currency_id')
    invoiced_amount = fields.Monetary(string='المبيعات', readonly=True)
    refunded_amount = fields.Monetary(string='المرتجعات', readonly=True)
    net_sales = fields.Monetary(string='صافي المبيعات', readonly=True)
    commission_amount = fields.Monetary(string='مبلغ العمولة', readonly=True)
