# -*- coding: utf-8 -*-
from odoo import models, fields


class AlraamlaaeSummaryLine(models.Model):
    _name = 'alramlaa.summary.line'
    _description = 'Al Ramlaa Quotation Summary Line'
    _order = 'sequence, id'

    order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(default=10)
    item_no = fields.Integer(string='Item No. / رقم البند')
    name = fields.Char(string='Description / الوصف', required=True)
    total = fields.Float(string='Total Price / الإجمالي', digits='Product Price')
