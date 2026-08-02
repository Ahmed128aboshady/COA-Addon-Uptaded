# -*- coding: utf-8 -*-
{
    'name': 'BOM Formula Calculator',
    'summary': 'إضافة حاسبة معادلات ديناميكية على BOM',
    'description': '\n        يضيف تاب "حاسبة التصنيع" على BOM يمكّنك من:\n        - تعريف متغيرات (طول، عرض، سماكة، عدد، ثوابت)\n        - كتابة معادلات Python يدوياً لكل component\n        - حساب الكميات تلقائياً وتحديث BOM Lines\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Manufacturing',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['mrp'],
    'data': ['security/ir.model.access.csv', 'views/bom_formula_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
