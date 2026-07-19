# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Account Restricted Access - COA',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Restrict accountant visibility to specific accounts in General Ledger and account moves.',
    'description': """
Account Restricted Access
==========================
This module allows defining a list of allowed accounts (Many2many) for each user in their user profile card.
Users belonging to the 'Restricted Accountant' group will only see and be able to access:

- Journal Items (account.move.line) for the allowed accounts only.
- General Ledger restricted to these accounts.
- Chart of Accounts restricted to these accounts only.

Developed by Community of Accountants (COA).
    """,
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'OPL-1',
    'depends': [
        'account',
    ],
    'data': [
        'security/account_restricted_security.xml',
        'security/account_restricted_rules.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 79.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
