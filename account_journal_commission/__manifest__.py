# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Journal Payment Commission',
    'version': '18.0.1.0.0',
    'summary': 'Add a configurable commission percentage on journal payment entries for specific accounts.',
    'author': 'Community of Accountants (COA)',
    'category': 'Accounting',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/account_payment_views.xml',
        'views/account_payment_register_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'website': 'https://coa-egy.odoo.com/',
    'price': 49.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
