# -*- coding: utf-8 -*-
{
    'name': 'Duplicate Company Data PRO',
    'summary': 'Seamlessly duplicate Chart of Accounts, Taxes, Journals, and Warehouses for Multi-Company Setup',
    'description': '\n        This module allows you to safely duplicate essential accounting and inventory configurations \n        from one company to another in a multi-company environment.\n        Fully compatible with Odoo 19 new shared accounts architecture.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base', 'account', 'stock'],
    'data': ['security/ir.model.access.csv', 'views/wizard_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
