# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Stock Reserved',
    'summary': 'Report of reserved stock by customer and product from sales orders, with unreserve button',
    'description': 'COA Sale Stock Reserved developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['security/ir.model.access.csv', 'views/sale_stock_reserved_views.xml', 'views/sale_stock_reserved_menu.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
