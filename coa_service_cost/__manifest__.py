# -*- coding: utf-8 -*-
{
    'name': 'COA Service Cost',
    'summary': 'For service products: redirects purchase bills to an Intermediate Account (instead of expensing immediately), then on...',
    'description': 'COA Service Cost developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account', 'product'],
    'data': ['views/product_template_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
