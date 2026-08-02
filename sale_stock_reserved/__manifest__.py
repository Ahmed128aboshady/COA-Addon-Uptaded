# -*- coding: utf-8 -*-
{
    'name': 'Sale Stock Reserved',
    'summary': 'Report of reserved stock by customer and product from sales orders, with unreserve button',
    'description': 'Professional Sale Stock Reserved custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['security/ir.model.access.csv', 'views/sale_stock_reserved_views.xml', 'views/sale_stock_reserved_menu.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
