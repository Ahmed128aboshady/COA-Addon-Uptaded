# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    milestone_line_ids = fields.One2many(
        'sale.milestone.payment.line',
        'payment_id',
        string='المراحل المرتبطة',
        readonly=True,
    )
    milestone_reconciled_amount = fields.Monetary(
        string='المُرحَّل على مراحل',
        compute='_compute_milestone_reconciled',
    )
    milestone_available_amount = fields.Monetary(
        string='المتاح للترحيل',
        compute='_compute_milestone_reconciled',
    )

    @api.depends('milestone_line_ids.amount', 'amount')
    def _compute_milestone_reconciled(self):
        for rec in self:
            reconciled = sum(rec.milestone_line_ids.mapped('amount'))
            rec.milestone_reconciled_amount = reconciled
            rec.milestone_available_amount = rec.amount - reconciled
