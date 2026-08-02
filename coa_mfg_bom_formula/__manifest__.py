# -*- coding: utf-8 -*-
{
    'name': 'COA Mfg Bom Formula',
    'summary': 'إضافة حاسبة معادلات ديناميكية على BOM',
    'description': 'COA Mfg Bom Formula developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Manufacturing',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['mrp'],
    'data': ['security/ir.model.access.csv', 'views/bom_formula_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
