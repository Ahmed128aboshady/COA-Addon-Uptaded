# -*- coding: utf-8 -*-
{
    'name': 'Location & Warehouse Code',
    'summary': 'Add code field to Location and Warehouse configuration',
    'description': "\n        This module adds a 'Code' field after the 'Name' field in:\n        - Stock Location configuration\n        - Warehouse configuration\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['views/stock_location_views.xml', 'views/stock_warehouse_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
