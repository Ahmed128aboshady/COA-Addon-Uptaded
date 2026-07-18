# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Order - Direct Invoice Print',
    'summary': 'Print the Sale Order invoice(s) directly from the SO with one click. Opens the browser print dialog immediately (no download). Works for Sales users without Accounting access.',
    'description': """
COA Sale Order - Direct Invoice Print
=====================================
- Adds a "Print Invoice" button on the Sale Order header.
- One click opens the invoice PDF and fires the browser print dialog
  automatically (inline preview, NOT a download).
- Salespeople can print the invoice even without Accounting access:
  access is validated on the Sale Order itself, then the invoice
  report is rendered server-side with elevated rights (safe scope:
  only invoices linked to that Sale Order).
- If the SO has multiple posted invoices, they are merged in one PDF.

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    """,
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'price': 19.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
