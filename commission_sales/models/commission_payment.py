# -*- coding: utf-8 -*-
from odoo import models, fields


class CommissionPayment(models.Model):
    _name = 'commission.payment'
    _description = 'دفعة عمولة'
    _order = 'date desc, id desc'

    name = fields.Char(string='المرجع', readonly=True, default='/')
    commission_id = fields.Many2one(
        'commission.line',
        string='سجل العمولة',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(string='تاريخ الدفع', required=True, default=fields.Date.today)
    amount = fields.Monetary(string='المبلغ المدفوع', required=True)
    currency_id = fields.Many2one(
        related='commission_id.currency_id',
        readonly=True,
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='حساب الدفع',
        required=True,
        domain=[('type', 'in', ['bank', 'cash'])],
    )
    memo = fields.Char(string='البيان / الملاحظة')
    move_id = fields.Many2one(
        'account.move',
        string='قيد الدفع',
        readonly=True,
        copy=False,
    )
