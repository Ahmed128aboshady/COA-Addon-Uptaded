# -*- coding: utf-8 -*-
{
    'name': 'COA Ts Location Restrictions',
    'summary': 'Restrict warehouse/stock locations and operation types per user',
    'description': 'COA Ts Location Restrictions developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '1.0.0',
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
