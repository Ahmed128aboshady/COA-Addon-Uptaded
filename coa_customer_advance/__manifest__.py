# -*- coding: utf-8 -*-
{
    'name': 'COA Customer Advance',
    'summary': 'دفعات مقدمة من العملاء في حساب التزام مستقل مع تسوية تلقائية ودعم مسار Down Payment من أمر البيع',
    'description': '\nCOA Customer Advance Payments\n=============================\nمساران للدفعة المقدمة:\n\n1. Payment مباشر (Accounting → Payments) مع خيار "Customer Advance":\n   القيد: من ح/ البنك إلى ح/ دفعات مقدمة (Liability) — وليس AR.\n\n2. من أمر البيع (Create Invoice → "Down payment (cash / bank)"):\n   يفتح نفس الشاشة لكن يسجّل Payment نقدي بقيد بنك/التزام بدل فاتورة،\n   ويربطه بأمر البيع، ويظهر كـ Outstanding Credit للتسوية مع الفاتورة.\n\n3. تسوية تدريجية عبر زر "تسوية دفعة مقدمة" على الفاتورة:\n   القيد: من ح/ دفعات مقدمة (Liability) إلى ح/ العملاء (AR) + reconcile.\n\nالدفعات في حساب التزام مستقل، فهي مستبعدة تلقائياً من إجمالي الإيراد.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '17.0.19.0.1.1.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['account', 'sale_management'],
    'data': ['security/ir.model.access.csv', 'data/account_advance_data.xml', 'wizard/advance_settle_wizard_views.xml', 'views/account_payment_views.xml', 'views/account_move_views.xml', 'views/sale_advance_payment_inv_views.xml', 'views/sale_order_views.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
