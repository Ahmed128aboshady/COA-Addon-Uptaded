# -*- coding: utf-8 -*-
{
    'name': 'COA Partner Ledger - Invoice Details Drill-down',
    'summary': 'Adds an expandable arrow next to each invoice in the Partner Ledger. Unfolding shows the invoice product lines with q...',
    'description': "\nCOA Partner Ledger - Invoice Details Drill-down\n===============================================\nExtends the Enterprise Partner Ledger report (account_reports) so that every\ninvoice / journal-item line becomes unfoldable. When you click its arrow, the\nreport expands into the invoice's PRODUCT LINES, showing:\n\n    Product name  -  Quantity (UoM)   |   Line Total\n\nHow it works (framework-safe):\n------------------------------\n* Inherits the report custom handler\n  'account.partner.ledger.report.handler'.\n* After the standard partner expansion runs, each move line that belongs to\n  an invoice is tagged unfoldable with a custom expand function.\n* Child (product) lines are built with the OFFICIAL\n  account.report._get_generic_line_id() helper - no hand-crafted line IDs,\n  so _parse_line_id never breaks.\n* No change to the account.report data record and no new columns: the line\n  total is rendered in the existing Balance column, and the quantity is shown\n  in the line label (the Partner Ledger has fixed Debit/Credit/Balance\n  columns).\n\nRequires: Odoo Enterprise (account_reports).\n\nDeveloped by Community of Accountants (COA)\nWhatsApp: +20 101 390 7174\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
    'license': 'OEEL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account_reports'],
    'data': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
