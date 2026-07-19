# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Sale: Stock Info in Product Search',
    'version': '18.0.1.0.0',
    'summary': 'Display real-time On Hand and available stock info inside the product search on sale orders.',
    'author': 'Community of Accountants (COA)',
    'category': 'Sales',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/sale_order_line_views.xml',
        'views/product_search_more_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'website': 'https://coa-egy.odoo.com/',
    'price': 29.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
