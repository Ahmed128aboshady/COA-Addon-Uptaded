# -*- coding: utf-8 -*-
{
    'name': 'Warehouse Location Restriction',
    'version': '19.0.1.0.0',
    'summary': 'Restrict warehouse/stock locations and operation types per user',
    'description': """
Warehouse Location Restriction
================================
Restrict inventory users' access to specific warehouses, transfer locations,
and operation types on an individual basis. Users can only access designated locations.
    """,
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory/Warehouse',
    'license': 'AGPL-3',
    'depends': ['stock', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
