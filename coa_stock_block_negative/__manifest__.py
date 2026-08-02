# -*- coding: utf-8 -*-
{
    'name': 'COA Stock Block Negative',
    'summary': 'Prevent stock levels from going negative anywhere in the system (manufacturing, deliveries, internal transfers, POS, ...',
    'description': 'Professional Block Negative Stock custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['security/stock_block_negative_security.xml', 'views/product_views.xml', 'views/stock_location_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
