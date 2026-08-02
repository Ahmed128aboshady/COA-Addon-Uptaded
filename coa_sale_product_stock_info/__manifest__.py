# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Product Stock Info',
    'summary': 'يظهر الكمية المتاحة والـ On Hand في سيرش المنتجات داخل المبيعات',
    'description': 'Professional Sale: Stock Info in Product Search custom module for Odoo.',
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
