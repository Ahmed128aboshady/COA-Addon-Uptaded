# -*- coding: utf-8 -*-
{
    'name': 'Reserved Qty Report',
    'summary': 'Report showing reserved products in sales orders',
    'description': 'Professional Reserved Qty Report custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['sale', 'stock', 'sale_stock'],
    'data': ['views/reserved_report_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
