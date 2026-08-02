# -*- coding: utf-8 -*-
{
    'name': 'COA Return Qty Control',
    'summary': 'Block returning more than the delivered quantity and show returned / remaining quantities on the return wizard and pi...',
    'description': 'Professional COA Return Quantity Control custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['views/stock_return_picking_views.xml', 'views/stock_picking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
