# -*- coding: utf-8 -*-
{
    'name': 'Sale Payment Milestones',
    'summary': 'شروط سداد بالمراحل مع ربط مباشر بالمدفوعات المحاسبية',
    'description': '\n        يتيح هذا الأدون للمبيعات تحديد جدول دفعات تفصيلي على أوردر البيع\n        (مثل 10% تعاقد، 25% بداية تصنيع، ...) وربطها بالمدفوعات الفعلية\n        المسجلة في المحاسبة دون الحاجة لإصدار فاتورة مسبقة.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_management', 'account'],
    'data': ['security/ir.model.access.csv', 'data/mail_template_data.xml', 'views/sale_payment_milestone_views.xml', 'views/sale_order_views.xml', 'wizard/milestone_reconcile_wizard_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
