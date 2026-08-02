# -*- coding: utf-8 -*-
{
    'name': 'Stock Disallow Negative',
    'summary': 'Disallow negative stock levels by default',
    'description': 'Professional Stock Disallow Negative custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '18.0.1.0.0',
    'license': 'AGPL-3',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['views/product_product_views.xml', 'views/stock_location_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
