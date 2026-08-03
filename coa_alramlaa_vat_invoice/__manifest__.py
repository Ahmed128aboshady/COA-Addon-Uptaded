# -*- coding: utf-8 -*-
{
    'name': 'COA Alramlaa Vat Invoice',
    'summary': 'Custom bilingual VAT Invoice PDF for Sale Orders',
    'description': 'COA Alramlaa Vat Invoice developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['report/ir_actions_report.xml', 'report/sale_order_invoice_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
