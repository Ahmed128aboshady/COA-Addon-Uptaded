# -*- coding: utf-8 -*-
{
    'name': 'COA Custom Date Order',
    'summary': 'Advanced Custom Date Order module for Odoo ERP.',
    'description': 'COA Custom Date Order developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '18.0.1.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale', 'purchase'],
    'data': ['views/sale_order_view.xml', 'views/purchase_order_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
