# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Partner Ledger - Invoice Details Drill-down',
    'summary': 'Adds an expandable drill-down arrow to view invoice lines in Partner Ledger.',
    'description': """Drill-Down: Adds an expandable arrow next to every invoice move line.
Invoice Details: Displays product name, quantities, and line totals directly within the ledger.
Native Integration: Works natively with account_reports without modifying core databases.
Credit Control: Perfect for credit control and detailed customer balance analysis.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
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
