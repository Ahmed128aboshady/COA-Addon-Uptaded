# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Order - Direct Invoice Print',
    'summary': 'Print the Sale Order invoice(s) directly from the SO with one click. Opens the browser print dialog immediately (no d...',
    'description': '\nCOA Sale Order - Direct Invoice Print\n=====================================\n- Adds a "Print Invoice" button on the Sale Order header.\n- One click opens the invoice PDF and fires the browser print dialog\n  automatically (inline preview, NOT a download).\n- Salespeople can print the invoice even without Accounting access:\n  access is validated on the Sale Order itself, then the invoice\n  report is rendered server-side with elevated rights (safe scope:\n  only invoices linked to that Sale Order).\n- If the SO has multiple posted invoices, they are merged in one PDF.\n\nDeveloped by Community of Accountants (COA)\nWhatsApp: +20 101 390 7174\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
