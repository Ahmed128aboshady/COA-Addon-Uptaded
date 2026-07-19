# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Sale Order - Direct Invoice Print',
    'summary': 'Print sale order invoices directly from the SO with one click.',
    'description': """Simplifies printing invoice documents directly from the sale order form:

Key Features:
* Adds a "Print Invoice" button directly on the Sale Order header.
* Opens the invoice PDF and launches the browser print dialog instantly.
* Enables salespeople to print invoices even without accounting permissions.""""Simplifies printing invoice documents directly from the sale order form:

Key Features:
* Adds a "Print Invoice" button directly on the Sale Order header.
* Opens the invoice PDF and launches the browser print dialog instantly.
* Enables salespeople to print invoices even without accounting permissions.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
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
