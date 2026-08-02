# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='res_users_allowed_account_rel',
        column1='user_id',
        column2='account_id',
        string='الحسابات المسموح بها',
        help='عند تحديد حسابات هنا (مع انتماء المستخدم لمجموعة "محاسب مقيّد '
             'الصلاحية")، لن يستطيع المستخدم رؤية أي حركة أو رصيد إلا لهذه '
             'الحسابات فقط في القيود ودفتر الأستاذ العام وشجرة الحسابات.',
    )

    is_restricted_accountant = fields.Boolean(
        string='محاسب مقيّد الصلاحية',
        compute='_compute_is_restricted_accountant',
        help='يُحسب تلقائيًا حسب انتماء المستخدم لمجموعة "محاسب مقيّد الصلاحية"',
    )

    def _compute_is_restricted_accountant(self):
        restricted_group = self.env.ref(
            'account_restricted_access.group_account_restricted',
            raise_if_not_found=False,
        )
        for user in self:
            user.is_restricted_accountant = bool(
                restricted_group and restricted_group in user.group_ids
            )
