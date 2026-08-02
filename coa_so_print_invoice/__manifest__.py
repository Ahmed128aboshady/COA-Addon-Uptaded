# -*- coding: utf-8 -*-
{
    'name': 'COA So Print Invoice',
    'summary': 'Print the Sale Order invoice(s) directly from the SO with one click. Opens the browser print dialog immediately (no d...',
    'description': 'COA So Print Invoice developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
