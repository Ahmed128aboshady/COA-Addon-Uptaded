# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_date_only = fields.Date(
        string='Quotation Date',
        compute='_compute_order_date_only',
        store=True,
    )

    @api.depends('order_date_only', 'date_order')
    def _compute_order_date_only(self):
        for rec in self:
            rec.order_date_only = rec.date_order.date() if rec.date_order else False
