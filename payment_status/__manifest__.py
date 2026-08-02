# -*- coding: utf-8 -*-
{
    'name': 'Payment Status on Delivery',
    'summary': 'Shows invoice payment status automatically on delivery orders',
    'description': 'Professional Payment Status on Delivery custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_stock', 'purchase_stock', 'account'],
    'data': ['views/stock_picking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
