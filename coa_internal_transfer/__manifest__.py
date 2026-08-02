# -*- coding: utf-8 -*-
{
    'name': 'COA Internal Transfer',
    'summary': 'Restore the classic Internal Transfer feature on Payments (Odoo 19)',
    'description': '\nCOA Accounting Internal Transfer\n=================================\nRestores the classic "Internal Transfer" workflow that existed on\naccount.payment before it was removed from Odoo core (Odoo 18/19).\n\nFeatures\n--------\n* Adds back "Internal Transfer" as a payment type, selectable from a new\n  Payment Type radio (Send / Receive / Internal Transfer).\n* Adds a "Destination Journal" field, shown only for internal transfers.\n* On confirmation, automatically creates a paired payment in the\n  destination journal and links both records.\n* Fully configurable Outstanding Accounts behaviour:\n    - If the source and destination journals use their own default\n      account as both Outstanding Receipts/Payments account, the\n      transfer is created directly reconciled (status = Paid).\n    - If dedicated Outstanding Accounts are configured on the journals,\n      the transfer is posted through those accounts and stays\n      "In Process" until reconciled with the bank statement.\n* A dedicated filter to list/find all internal transfers.\n\nDeveloped by Community of Accountants (COA) - Odoo Silver Partner.\n',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['views/account_payment_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
