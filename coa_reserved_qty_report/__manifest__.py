# -*- coding: utf-8 -*-
{
    'name': 'COA Reserved Qty Report',
    'summary': 'Report showing reserved products in sales orders',
    'description': 'COA Reserved Qty Report developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['sale', 'stock', 'sale_stock'],
    'data': ['views/reserved_report_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
