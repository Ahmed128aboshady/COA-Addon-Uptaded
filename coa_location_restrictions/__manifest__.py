# -*- coding: utf-8 -*-
{
    'name': 'Warehouse Location & Operation Restriction',
    'version': '19.0.1.0.2',
    'summary': 'Restrict inventory operations and stock moves to allowed warehouses and locations.',
    'description': """Limits user access to specific warehouses, locations, and picking operation types:

Key Features:
* Configurable location permissions tab inside User profile.
* Restricts stock picking, validating, and viewing of moves at unauthorized locations.
* Automatically filters stock quants so users only see quantities in allowed places.
* Fully compatible with recursive locations and multi-warehouse operations.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'category': 'Inventory/Warehouse',
    'license': 'OPL-1',
    'depends': ['stock', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/stock_picking_views.xml',
    ],
    'price': 99.00,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
