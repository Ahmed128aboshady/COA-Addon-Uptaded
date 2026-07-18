# -*- coding: utf-8 -*-
{
    'name': 'COA Partner Ledger - Invoice Details Drill-down',
    'summary': 'Adds an expandable arrow next to each invoice in the Partner Ledger. Unfolding shows the invoice product lines with quantity and total.',
    'description': """
COA Partner Ledger - Invoice Details Drill-down
===============================================
Extends the Enterprise Partner Ledger report (account_reports) so that every
invoice / journal-item line becomes unfoldable. When you click its arrow, the
report expands into the invoice's PRODUCT LINES, showing:

    Product name  -  Quantity (UoM)   |   Line Total

How it works (framework-safe):
------------------------------
* Inherits the report custom handler
  'account.partner.ledger.report.handler'.
* After the standard partner expansion runs, each move line that belongs to
  an invoice is tagged unfoldable with a custom expand function.
* Child (product) lines are built with the OFFICIAL
  account.report._get_generic_line_id() helper - no hand-crafted line IDs,
  so _parse_line_id never breaks.
* No change to the account.report data record and no new columns: the line
  total is rendered in the existing Balance column, and the quantity is shown
  in the line label (the Partner Ledger has fixed Debit/Credit/Balance
  columns).

Requires: Odoo Enterprise (account_reports).

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    """,
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
    'category': 'Accounting/Accounting',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'depends': [
        'account_reports',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'price': 69.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
