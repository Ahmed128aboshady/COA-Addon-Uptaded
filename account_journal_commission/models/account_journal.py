# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # ===== فواتير المبيعات =====
    sale_has_commission = fields.Boolean(
        string='تفعيل عمولة على فواتير المبيعات',
        default=False,
    )
    sale_commission_rate = fields.Float(
        string='نسبة عمولة المبيعات %',
        default=0.0,
        digits=(5, 4),
        help='مثال: 1 = 1% — بيتخصم من سداد فواتير المبيعات'
    )

    # ===== فواتير المشتريات =====
    purchase_has_commission = fields.Boolean(
        string='تفعيل عمولة على فواتير المشتريات',
        default=False,
    )
    purchase_commission_rate = fields.Float(
        string='نسبة عمولة المشتريات %',
        default=0.0,
        digits=(5, 4),
        help='مثال: 1 = 1% — بيتخصم من سداد فواتير المشتريات'
    )
