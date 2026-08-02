# -*- coding: utf-8 -*-
{
    'name': 'COA Alramlaa Company Duplicator',
    'summary': 'Seamlessly duplicate Chart of Accounts, Taxes, Journals, and Warehouses for Multi-Company Setup',
    'description': 'COA Alramlaa Company Duplicator developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
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
