# -*- coding: utf-8 -*-
{
    'name': 'COA Account Merge',
    'summary': 'Merge two or more GL accounts while preserving full journal ledger history.all journal items and references move to o...',
    'description': 'COA Account Merge developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['security/ir.model.access.csv', 'views/account_merge_wizard_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
