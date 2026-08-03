# -*- coding: utf-8 -*-
{
    'name': 'COA Account Journal Commission',
    'summary': 'Enterprise-grade Account Journal Commission solution for Odoo Accounting. Streamlines workflow execution, automates journal validations, and delivers real-time business insights.',
    'description': 'COA Account Journal Commission developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['security/ir.model.access.csv', 'views/account_journal_views.xml', 'views/account_payment_views.xml', 'views/account_payment_register_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
