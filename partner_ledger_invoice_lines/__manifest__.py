# -*- coding: utf-8 -*-
{
    'name': 'Partner Ledger Invoice Lines',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Reporting',
    'summary': 'Display invoice lines details in Partner Ledger Report',
    'description': """
Partner Ledger Invoice Lines
=============================

This module extends the Partner Ledger Report to display invoice line items
(products) under each invoice entry in an expandable/collapsible format.

Features:
---------
* Expandable invoice lines under each invoice/bill entry
* Display product name, quantity, unit price
* Show amounts in Debit/Credit/Balance columns
* Support for all invoice types (invoices, bills, refunds)
* Clean and professional formatting
* Maintains report performance with on-demand loading

Usage:
------
1. Go to Accounting > Reporting > Partner Ledger
2. Expand any partner line to see their invoices
3. Click the expand icon on any invoice to see its line items
4. Each line shows: Product | Qty × Price with amounts

Technical:
----------
* Inherits: account.partner.ledger.report.handler
* Adds unfoldable functionality to move lines
* Custom expand function for invoice lines
* Filters only product lines (excludes sections/notes)

""",
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'license': 'LGPL-3',
    'depends': [
        'account_reports',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
