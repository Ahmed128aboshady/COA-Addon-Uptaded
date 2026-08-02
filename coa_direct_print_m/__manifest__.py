# -*- coding: utf-8 -*-
{
    'name': 'COA Direct Print - SO / Invoice / Customer Statement',
    'summary': 'One-click direct printing (browser print dialog, no download) for Sale Orders, Customer Invoices, and Customer Statem...',
    'description': "\nCOA Direct Print\n================\nOne click = print dialog opens immediately. No download, no extra steps.\n\nButtons added:\n--------------\n* Sale Order form:\n    - Print Order      : the Quotation / Order PDF\n    - Print Invoice    : all posted invoices of this SO (merged in one PDF)\n    - Customer Statement : full receivable statement of the SO customer\n* Invoice form (customer invoices):\n    - Direct Print     : the invoice PDF\n    - Customer Statement\n* Partner form:\n    - Customer Statement\n\nCustomer Statement (كشف حساب العميل):\n-------------------------------------\nCustom QWeb statement built from posted receivable journal items,\nwith running balance and total due. Works on Community & Enterprise.\n\nPermissions:\n------------\nAccess is validated on the source record (SO / Invoice / Partner).\nRendering then runs with elevated rights limited to that record's\ndata only - Sales users can print invoices & statements without\nbeing granted Accounting access.\n\nPrinting technique:\n-------------------\nThe PDF is fetched as a blob and loaded into a hidden iframe, then\nthe browser print dialog is triggered (same technique as print.js -\nreliable on Chrome/Edge). A visible preview + manual Print button\nare always available as fallback.\n\nDeveloped by Community of Accountants (COA)\nWhatsApp: +20 101 390 7174\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['report/partner_statement_report.xml', 'report/partner_statement_templates.xml', 'report/payment_receipt_report.xml', 'report/payment_receipt_templates.xml', 'views/sale_order_views.xml', 'views/account_move_views.xml', 'views/account_payment_views.xml', 'views/res_partner_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
