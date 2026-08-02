# -*- coding: utf-8 -*-
{
    'name': 'COA Location Warehouse Code',
    'summary': 'Add code field to Location and Warehouse configuration',
    'description': 'COA Location Warehouse Code developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['views/stock_location_views.xml', 'views/stock_warehouse_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
