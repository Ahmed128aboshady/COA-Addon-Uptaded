# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    commission_journal_id = fields.Many2one(
        'account.journal',
        string='يومية العمولات',
        domain=[('type', 'in', ['general', 'miscellaneous'])],
        help='اليومية الافتراضية لقيود استحقاق العمولات.',
    )
    commission_debit_account_id = fields.Many2one(
        'account.account',
        string='حساب المدين الافتراضي',
        help='حساب المدين الافتراضي لقيود العمولات، مثال: مصروف عمولات.',
    )
    commission_credit_account_id = fields.Many2one(
        'account.account',
        string='حساب الدائن الافتراضي',
        help='حساب الدائن الافتراضي لقيود العمولات، مثال: عمولات مستحقة الدفع.',
    )
    commission_own_documents = fields.Boolean(
        string='Own Documents Only',
        default=False,
        help='عند التفعيل: كل مندوب يرى سجلات عمولاته هو فقط. المديرون يرون الكل دائماً.',
    )
