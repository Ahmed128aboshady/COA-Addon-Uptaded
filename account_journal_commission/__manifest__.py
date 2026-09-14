# -*- coding: utf-8 -*-
{
    'website': 'https://www.coa-egy.com',
    'name': 'Journal Payment Commission',
    'version': '19.0.1.0.0',
    'summary': 'خصم عمولة تلقائي على الـ Journal - مبيعات ومشتريات منفصلين',
    'author': 'Community of accountants (COA-Egypt)',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/account_payment_views.xml',
        'views/account_payment_register_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
