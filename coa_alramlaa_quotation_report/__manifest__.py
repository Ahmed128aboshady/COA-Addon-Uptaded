# -*- coding: utf-8 -*-
{
    'name': 'COA Alramlaa Quotation Report',
    'summary': 'Custom Quotation/Sales Order PDF Report - Al Ramlaa Wooden Products Style',
    'description': 'COA Alramlaa Quotation Report developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['security/ir.model.access.csv', 'report/quotation_report.xml', 'report/quotation_report_template.xml', 'views/sale_order_views.xml', 'views/product_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
