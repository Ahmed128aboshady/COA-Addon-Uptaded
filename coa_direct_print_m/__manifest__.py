# -*- coding: utf-8 -*-
{
    'name': 'COA Direct Print M',
    'summary': 'One-click direct printing (browser print dialog, no download) for Sale Orders, Customer Invoices, and Customer Statem...',
    'description': 'COA Direct Print M developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['report/partner_statement_report.xml', 'report/partner_statement_templates.xml', 'report/payment_receipt_report.xml', 'report/payment_receipt_templates.xml', 'views/sale_order_views.xml', 'views/account_move_views.xml', 'views/account_payment_views.xml', 'views/res_partner_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
