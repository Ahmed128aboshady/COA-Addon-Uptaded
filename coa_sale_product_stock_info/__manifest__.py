# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Product Stock Info',
    'summary': 'يظهر الكمية المتاحة والـ On Hand في سيرش المنتجات داخل المبيعات',
    'description': 'COA Sale Product Stock Info developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
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
