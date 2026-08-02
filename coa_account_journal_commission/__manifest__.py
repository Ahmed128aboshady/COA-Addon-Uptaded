# -*- coding: utf-8 -*-
{
    'name': 'COA Account Journal Commission',
    'summary': 'خصم عمولة تلقائي على الـ Journal - مبيعات ومشتريات منفصلين',
    'description': 'COA Account Journal Commission developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
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
