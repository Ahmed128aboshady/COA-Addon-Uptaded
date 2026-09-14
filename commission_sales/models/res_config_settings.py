# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_journal_id = fields.Many2one(
        related='company_id.commission_journal_id',
        string='يومية العمولات',
        readonly=False,
    )
    commission_debit_account_id = fields.Many2one(
        related='company_id.commission_debit_account_id',
        string='حساب المدين الافتراضي',
        readonly=False,
    )
    commission_credit_account_id = fields.Many2one(
        related='company_id.commission_credit_account_id',
        string='حساب الدائن الافتراضي',
        readonly=False,
    )
    commission_own_documents = fields.Boolean(
        related='company_id.commission_own_documents',
        string='Own Documents Only',
        readonly=False,
    )
