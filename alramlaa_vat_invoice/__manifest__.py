# -*- coding: utf-8 -*-
{
    'name': 'Alramlaa VAT Invoice Report',
    'summary': 'Custom bilingual VAT Invoice PDF for Sale Orders',
    'description': 'Professional bilingual (Arabic/English) VAT Invoice report for Sale Orders',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['report/ir_actions_report.xml', 'report/sale_order_invoice_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
