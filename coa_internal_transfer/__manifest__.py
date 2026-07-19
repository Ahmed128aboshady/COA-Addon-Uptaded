# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Accounting Internal Transfer',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Restore the classic Internal Transfer feature on Payments screen.',
    'description': """Restores the popular "Internal Transfer" payment type on Payments (account.payment):

Key Features:
* Adds a new "Internal Transfer" option to Payment Type selection.
* Adds a "Destination Journal" field for transfers.
* Automatically generates paired payment entries to reconcile both sides.
* Supports outstanding receipt/payment account reconciliation.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'OPL-1',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_payment_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 49.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
