# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOperationStage(models.Model):
    _name = 'sale.operation.stage'
    _description = 'مراحل العمليات'
    _order = 'sequence, id'

    name = fields.Char(
        string='اسم المرحلة',
        required=True,
        translate=True,
    )
    sequence = fields.Integer(
        string='الترتيب',
        default=10,
    )
    code = fields.Char(
        string='كود المرحلة',
        help='كود مختصر للمرحلة'
    )
    description = fields.Text(
        string='وصف المرحلة',
    )
    responsible_group_id = fields.Many2one(
        'res.groups',
        string='المجموعة المسؤولة',
        help='المجموعة اللي عندها صلاحية تأكيد المرحلة دي'
    )
    is_first = fields.Boolean(
        string='مرحلة البداية',
        default=False,
        help='أول مرحلة بعد الاستلام من المبيعات'
    )
    is_last = fields.Boolean(
        string='مرحلة نهائية',
        default=False,
        help='لما تتأكد — بيفتح التسليم للعميل'
    )
    color = fields.Integer(
        string='اللون',
        default=0,
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'اسم المرحلة لازم يكون فريد!'),
    ]
