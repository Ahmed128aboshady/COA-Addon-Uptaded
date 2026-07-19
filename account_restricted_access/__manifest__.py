# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Account Restricted Access - COA',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Restrict accountant visibility to specific General Ledger accounts.',
    'description': """This module restricts accountants to view and edit only their assigned accounts.

Key Features:
* Configure a list of allowed accounts directly on the User Form (Many2many).
* Restricts access to Journal Items (account.move.line) to only allowed accounts.
* Restricts General Ledger report views to permitted accounts.
* Filters the Chart of Accounts recursively based on user settings.
* Fully compatible with multi-company environments.""""This module restricts accountants to view and edit only their assigned accounts.

Key Features:
* Configure a list of allowed accounts directly on the User Form (Many2many).
* Restricts access to Journal Items (account.move.line) to only allowed accounts.
* Restricts General Ledger report views to permitted accounts.
* Filters the Chart of Accounts recursively based on user settings.
* Fully compatible with multi-company environments.""",
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
