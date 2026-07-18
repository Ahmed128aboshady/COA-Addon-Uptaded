# -*- coding: utf-8 -*-
{
    'name': 'Sale: Stock Info in Product Search',
    'version': '18.0.1.0.0',
    'summary': 'يظهر الكمية المتاحة والـ On Hand في سيرش المنتجات داخل المبيعات',
    'author': 'Community of Accountants',
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
    'license': 'LGPL-3',
    'website': 'https://www.communityofaccountants.com',
    'price': 29.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
