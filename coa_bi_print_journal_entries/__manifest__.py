# -*- coding: utf-8 -*-
{
    'name': 'COA Bi Print Journal Entries',
    'summary': 'Allow to print pdf report of Journal Entries.',
    'description': 'COA Bi Print Journal Entries developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.19.0.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['base', 'account'],
    'data': ['report/report_journal_entries.xml', 'report/report_journal_entries_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
