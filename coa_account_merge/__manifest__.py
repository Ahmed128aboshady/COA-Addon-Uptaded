# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Account Merge',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Merge two or more GL accounts while preserving full journal ledger history.'
               'all journal items and references move to one account.',
    'description': """Adds a "Merge Accounts" action on the Chart of Accounts list view:

Key Features:
* Select two or more accounts, select a destination account, and merge.
* Re-points all historical Journal Items to the destination account.
* Keeps chronological date order and running balances completely intact.
* Updates all default accounting rules, tax rules, product models, and partner records.
* Archives source accounts safely instead of deleting them.""""Adds a "Merge Accounts" action on the Chart of Accounts list view:

Key Features:
* Select two or more accounts, select a destination account, and merge.
* Re-points all historical Journal Items to the destination account.
* Keeps chronological date order and running balances completely intact.
* Updates all default accounting rules, tax rules, product models, and partner records.
* Archives source accounts safely instead of deleting them.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_merge_wizard_views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
