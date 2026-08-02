# -*- coding: utf-8 -*-
{
    'name': 'COA Location Restrictions',
    'summary': 'Restrict inventory operations and stock moves to allowed warehouses and locations.',
    'description': 'COA Location Restrictions developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.1.0.2.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
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
