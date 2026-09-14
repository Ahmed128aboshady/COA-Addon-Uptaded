# -*- coding: utf-8 -*-
{
    'name': 'COA Sales Order Tracking Report',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'متابعة أوامر البيع: كميات التصنيع والتسليم والفوترة لكل صنف',
    'description': """
COA Sales Order Tracking Report
===============================
لوحة تحكم تفاعلية لمتابعة أوامر البيع من البداية للنهاية:
- قائمة أوامر البيع قابلة للتوسيع (drop-list)
- لكل أمر بيع: تفاصيل كل صنف بالكمية (مطلوب / تم / متبقي)
- التصنيع: كمية تم تصنيعها + نسبة + المتبقي
- التسليم: كمية تم تسليمها + نسبة + المتبقي
- الفوترة: كمية تم فوترتها + نسبة + المتبقي
    """,
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'depends': ['sale', 'mrp', 'sale_mrp'],
    'data': [
        'views/so_tracking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'coa_so_tracking/static/src/scss/so_dashboard.scss',
            'coa_so_tracking/static/src/js/so_dashboard.js',
            'coa_so_tracking/static/src/xml/so_dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
