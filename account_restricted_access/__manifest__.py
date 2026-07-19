# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Account Restricted Access - COA',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'تقييد رؤية المحاسب على حسابات معينة في الجينرال ليدجر وحركة الحسابات',
    'description': """
Account Restricted Access
==========================
يسمح هذا الموديول بتحديد قائمة حسابات (Many2many) لكل مستخدم من خلال بطاقة
المستخدم (Users). المستخدم المنتمي لمجموعة "محاسب مقيّد الصلاحية" لن يرى
ولن يستطيع الوصول إلا إلى:

- حركة القيود (Journal Items / account.move.line) الخاصة بالحسابات المسموح بها فقط
- دفتر الأستاذ العام (General Ledger) محدود بهذه الحسابات
- شجرة الحسابات (Chart of Accounts) محدودة بهذه الحسابات فقط

تم تطويره بواسطة Community of Accountants - COA
Odoo Silver Partner
    """,
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'OPL-1',
    'depends': [
        'account',
    ],
    'data': [
        'security/account_restricted_security.xml',
        'security/account_restricted_rules.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 79.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
