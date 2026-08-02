# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Order Return',
    'summary': 'Create return transfers directly from sales orders',
    'description': 'COA Sale Order Return developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['security/ir.model.access.csv', 'wizard/sale_return_wizard_views.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
