# -*- coding: utf-8 -*-
{
    'name': 'COA Customer Advance Payments',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'دفعات مقدمة من العملاء في حساب التزام مستقل مع تسوية تلقائية '
               'ودعم مسار Down Payment من أمر البيع',
    'description': """
COA Customer Advance Payments
=============================
مساران للدفعة المقدمة:

1. Payment مباشر (Accounting → Payments) مع خيار "Customer Advance":
   القيد: من ح/ البنك إلى ح/ دفعات مقدمة (Liability) — وليس AR.

2. من أمر البيع (Create Invoice → "Down payment (cash / bank)"):
   يفتح نفس الشاشة لكن يسجّل Payment نقدي بقيد بنك/التزام بدل فاتورة،
   ويربطه بأمر البيع، ويظهر كـ Outstanding Credit للتسوية مع الفاتورة.

3. تسوية تدريجية عبر زر "تسوية دفعة مقدمة" على الفاتورة:
   القيد: من ح/ دفعات مقدمة (Liability) إلى ح/ العملاء (AR) + reconcile.

الدفعات في حساب التزام مستقل، فهي مستبعدة تلقائياً من إجمالي الإيراد.
    """,
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'depends': ['account', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'data/account_advance_data.xml',
        'wizard/advance_settle_wizard_views.xml',
        'views/account_payment_views.xml',
        'views/account_move_views.xml',
        'views/sale_advance_payment_inv_views.xml',
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
