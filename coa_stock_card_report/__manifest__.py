# -*- coding: utf-8 -*-
{
    'name': 'COA Stock Card Report',
    'summary': 'Stock card report with running balance per product and location',
    'description': 'COA Stock Card Report developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['security/ir.model.access.csv', 'views/stock_card_wizard_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
