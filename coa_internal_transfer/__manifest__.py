# -*- coding: utf-8 -*-
{
    'name': 'COA Accounting Internal Transfer',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Restore the classic Internal Transfer feature on Payments (Odoo 19)',
    'description': """
COA Accounting Internal Transfer
=================================
Restores the classic "Internal Transfer" workflow that existed on
account.payment before it was removed from Odoo core (Odoo 18/19).

Features
--------
* Adds back "Internal Transfer" as a payment type, selectable from a new
  Payment Type radio (Send / Receive / Internal Transfer).
* Adds a "Destination Journal" field, shown only for internal transfers.
* On confirmation, automatically creates a paired payment in the
  destination journal and links both records.
* Fully configurable Outstanding Accounts behaviour:
    - If the source and destination journals use their own default
      account as both Outstanding Receipts/Payments account, the
      transfer is created directly reconciled (status = Paid).
    - If dedicated Outstanding Accounts are configured on the journals,
      the transfer is posted through those accounts and stays
      "In Process" until reconciled with the bank statement.
* A dedicated filter to list/find all internal transfers.

Developed by Community of Accountants (COA) - Odoo Silver Partner.
""",
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
    'license': 'LGPL-3',
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
