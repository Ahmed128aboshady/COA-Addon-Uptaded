# -*- coding: utf-8 -*-
{
    'name': 'Partner Ledger Invoice Lines',
    'summary': 'Display invoice lines details in Partner Ledger Report',
    'description': '\nPartner Ledger Invoice Lines\n=============================\n\nThis module extends the Partner Ledger Report to display invoice line items\n(products) under each invoice entry in an expandable/collapsible format.\n\nFeatures:\n---------\n* Expandable invoice lines under each invoice/bill entry\n* Display product name, quantity, unit price\n* Show amounts in Debit/Credit/Balance columns\n* Support for all invoice types (invoices, bills, refunds)\n* Clean and professional formatting\n* Maintains report performance with on-demand loading\n\nUsage:\n------\n1. Go to Accounting > Reporting > Partner Ledger\n2. Expand any partner line to see their invoices\n3. Click the expand icon on any invoice to see its line items\n4. Each line shows: Product | Qty × Price with amounts\n\nTechnical:\n----------\n* Inherits: account.partner.ledger.report.handler\n* Adds unfoldable functionality to move lines\n* Custom expand function for invoice lines\n* Filters only product lines (excludes sections/notes)\n\n',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.1.4',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account_reports'],
    'data': ['security/ir.model.access.csv'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
