# -*- coding: utf-8 -*-
{
    'website': 'https://www.coa-egy.com',
    'name': 'Sale: Stock Info in Product Search',
    'version': '19.0.1.0.0',
    'summary': 'يظهر الكمية المتاحة والـ On Hand في سيرش المنتجات داخل المبيعات',
    'author': 'Community of accountants (COA-Egypt)',
    'category': 'Sales',
    'depends': ['sale_stock'],
    'data': [
        'views/sale_order_line_views.xml',
        'views/product_search_more_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
