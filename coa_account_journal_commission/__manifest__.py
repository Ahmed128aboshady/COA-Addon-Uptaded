# -*- coding: utf-8 -*-
{
    'name': 'COA Account Journal Commission',
    'summary': 'خصم عمولة تلقائي على الـ Journal - مبيعات ومشتريات منفصلين',
    'description': 'Professional Journal Payment Commission custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
