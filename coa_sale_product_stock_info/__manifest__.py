# -*- coding: utf-8 -*-
{
    'name': 'Sale: Stock Info in Product Search',
    'summary': 'Display real-time On Hand and available stock inside the sale product search.',
    'description': 'Product Search: Displays product stock (On Hand / Available) inside the search list view.\nSales Integration: Seamlessly integrates with Odoo sales portal and backend forms.\nStock Availability: Helps sales reps verify stock status directly from sale order lines.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['views/sale_order_line_views.xml', 'views/product_search_more_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
