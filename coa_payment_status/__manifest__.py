# -*- coding: utf-8 -*-
{
    'name': 'COA Payment Status',
    'summary': 'Shows invoice payment status automatically on delivery orders',
    'description': 'COA Payment Status developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_stock', 'purchase_stock', 'account'],
    'data': ['views/stock_picking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
