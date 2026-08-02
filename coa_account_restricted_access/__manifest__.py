# -*- coding: utf-8 -*-
{
    'name': 'COA Account Restricted Access',
    'summary': 'تقييد رؤية المحاسب على حسابات معينة في الجينرال ليدجر وحركة الحسابات',
    'description': '\nAccount Restricted Access\n==========================\nيسمح هذا الموديول بتحديد قائمة حسابات (Many2many) لكل مستخدم من خلال بطاقة\nالمستخدم (Users). المستخدم المنتمي لمجموعة "محاسب مقيّد الصلاحية" لن يرى\nولن يستطيع الوصول إلا إلى:\n\n- حركة القيود (Journal Items / account.move.line) الخاصة بالحسابات المسموح بها فقط\n- دفتر الأستاذ العام (General Ledger) محدود بهذه الحسابات\n- شجرة الحسابات (Chart of Accounts) محدودة بهذه الحسابات فقط\n\nتم تطويره بواسطة Community of Accountants - COA\nOdoo Silver Partner\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['security/account_restricted_security.xml', 'security/account_restricted_rules.xml', 'security/ir.model.access.csv', 'views/res_users_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
