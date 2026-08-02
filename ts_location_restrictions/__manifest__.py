# -*- coding: utf-8 -*-
{
    'name': 'Warehouse Location Restriction',
    'summary': 'Restrict warehouse/stock locations and operation types per user',
    'description': "\nWarehouse Location Restriction\n================================\nRestrict inventory users' access to specific warehouses, transfer locations,\nand operation types on an individual basis. Users can only access designated locations.\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'AGPL-3',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock', 'mail'],
    'data': ['security/security.xml', 'security/ir.model.access.csv', 'views/res_users_views.xml', 'views/stock_picking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
