# -*- coding: utf-8 -*-
{
    'name': 'Al Ramlaa Quotation Report',
    'summary': 'Custom Quotation/Sales Order PDF Report - Al Ramlaa Wooden Products Style',
    'description': '\n        Custom QWeb PDF report for Quotations and Sales Orders.\n        Includes:\n        - Company header with logo\n        - Quotation summary page\n        - Detailed item pages with images, descriptions, materials, dimensions, qty & prices\n        - Joinery section\n        - Furniture section\n        - Payment terms & delivery terms\n        - Arabic + English bilingual support\n        - Footer with company info\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['security/ir.model.access.csv', 'report/quotation_report.xml', 'report/quotation_report_template.xml', 'views/sale_order_views.xml', 'views/product_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
