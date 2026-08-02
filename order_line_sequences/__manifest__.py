# -*- coding: utf-8 -*-
{
    'name': 'Order Line Sequences/Line Numbers',
    'summary': 'Sequence numbers in order lines of sales,purchase and delivery.',
    'description': 'This module will help you to add sequence for order lines\n    in sales, purchase and delivery. It will also add line numbers in report lines.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'AGPL-3',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['base', 'sale_management', 'purchase', 'stock'],
    'data': ['views/sale_order_views.xml', 'views/purchase_order_views.xml', 'views/stock_picking_views.xml', 'views/sale_order_templates.xml', 'views/stock_picking_templates.xml', 'views/purchase_order_templates.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
