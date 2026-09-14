# -*- coding: utf-8 -*-
{
    'name': 'COA Direct Print - SO / Invoice / Customer Statement',
    'summary': 'One-click direct printing (browser print dialog, no download) '
               'for Sale Orders, Customer Invoices, and Customer Statement '
               '(Partner Ledger style). Sales users can print without '
               'Accounting access.',
    'description': """
COA Direct Print
================
One click = print dialog opens immediately. No download, no extra steps.

Buttons added:
--------------
* Sale Order form:
    - Print Order      : the Quotation / Order PDF
    - Print Invoice    : all posted invoices of this SO (merged in one PDF)
    - Customer Statement : full receivable statement of the SO customer
* Invoice form (customer invoices):
    - Direct Print     : the invoice PDF
    - Customer Statement
* Partner form:
    - Customer Statement

Customer Statement (كشف حساب العميل):
-------------------------------------
Custom QWeb statement built from posted receivable journal items,
with running balance and total due. Works on Community & Enterprise.

Permissions:
------------
Access is validated on the source record (SO / Invoice / Partner).
Rendering then runs with elevated rights limited to that record's
data only - Sales users can print invoices & statements without
being granted Accounting access.

Printing technique:
-------------------
The PDF is fetched as a blob and loaded into a hidden iframe, then
the browser print dialog is triggered (same technique as print.js -
reliable on Chrome/Edge). A visible preview + manual Print button
are always available as fallback.

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    """,
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['sale', 'account'],
    'data': [
        'report/partner_statement_report.xml',
        'report/partner_statement_templates.xml',
        'report/payment_receipt_report.xml',
        'report/payment_receipt_templates.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
}
