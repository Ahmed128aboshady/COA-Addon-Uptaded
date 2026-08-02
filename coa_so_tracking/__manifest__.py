# -*- coding: utf-8 -*-
{
    'name': 'COA Sales Order Tracking Report',
    'summary': 'متابعة أوامر البيع: كميات التصنيع والتسليم والفوترة لكل صنف',
    'description': '\nCOA Sales Order Tracking Report\n===============================\nلوحة تحكم تفاعلية لمتابعة أوامر البيع من البداية للنهاية:\n- قائمة أوامر البيع قابلة للتوسيع (drop-list)\n- لكل أمر بيع: تفاصيل كل صنف بالكمية (مطلوب / تم / متبقي)\n- التصنيع: كمية تم تصنيعها + نسبة + المتبقي\n- التسليم: كمية تم تسليمها + نسبة + المتبقي\n- الفوترة: كمية تم فوترتها + نسبة + المتبقي\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.1.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['sale', 'mrp', 'sale_mrp'],
    'data': ['views/so_tracking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
