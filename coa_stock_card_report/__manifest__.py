# -*- coding: utf-8 -*-
{
    'name': 'COA Stock Card Report',
    'summary': 'Stock card report with running balance per product and location',
    'description': 'Professional Stock Card Report custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
