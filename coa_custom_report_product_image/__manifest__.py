# -*- coding: utf-8 -*-
{
    'name': 'COA Custom Report Product Image',
    'summary': 'Adds product image to Delivery prints and splits product name / reference code into separate columns across all modul...',
    'description': 'COA Custom Report Product Image developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['stock', 'sale_management', 'purchase', 'account'],
    'data': ['report/report_delivery_custom.xml', 'report/report_sale_custom.xml', 'report/report_purchase_custom.xml', 'report/report_invoice_custom.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
