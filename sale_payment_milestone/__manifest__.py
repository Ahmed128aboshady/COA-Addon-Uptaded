# -*- coding: utf-8 -*-
{
    'name': 'Sale Payment Milestones',
    'version': '19.0.1.0.0',
    'summary': 'شروط سداد بالمراحل مع ربط مباشر بالمدفوعات المحاسبية',
    'description': """
        يتيح هذا الأدون للمبيعات تحديد جدول دفعات تفصيلي على أوردر البيع
        (مثل 10% تعاقد، 25% بداية تصنيع، ...) وربطها بالمدفوعات الفعلية
        المسجلة في المحاسبة دون الحاجة لإصدار فاتورة مسبقة.
    """,
    'author': 'COA (Community of Accountants)',
    'category': 'Sales/Sales',
    'depends': ['sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/sale_payment_milestone_views.xml',
        'views/sale_order_views.xml',
        'wizard/milestone_reconcile_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
