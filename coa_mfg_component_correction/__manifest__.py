# -*- coding: utf-8 -*-
{
    'name': 'COA Mfg Component Correction',
    'summary': 'تصحيح كميات المكونات بعد إتمام أوامر التصنيع',
    'description': '\n        يتيح هذا الموديول إمكانية تصحيح كميات المكونات المستهلكة\n        بعد إغلاق أمر التصنيع، مع إرجاع الفارق للمخزن وتصحيح التكلفة تلقائياً.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Manufacturing',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['mrp', 'stock', 'stock_account'],
    'data': ['security/ir.model.access.csv', 'wizard/mrp_component_correction_wizard_view.xml', 'views/mrp_production_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
