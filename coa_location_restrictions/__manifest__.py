# -*- coding: utf-8 -*-
{
    'name': 'COA Location Restrictions',
    'summary': 'Restrict inventory operations and stock moves to allowed warehouses and locations.',
    'description': 'Permissions Tab: Configurable location permissions tab inside User profile.\nLocation Security: Restricts stock picking, validating, and viewing of moves at unauthorized locations.\nQuant Filtering: Automatically filters stock quants so users only see quantities in allowed places.\nRecursive Scoping: Fully compatible with recursive locations and multi-warehouse operations.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.2',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock', 'mail'],
    'data': ['security/security.xml', 'security/ir.model.access.csv', 'views/res_users_views.xml', 'views/stock_picking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
