# -*- coding: utf-8 -*-
{
    'name': 'Al Ramlaa Quotation Report',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom Quotation/Sales Order PDF Report - Al Ramlaa Wooden Products Style',
    'description': """
        Custom QWeb PDF report for Quotations and Sales Orders.
        Includes:
        - Company header with logo
        - Quotation summary page
        - Detailed item pages with images, descriptions, materials, dimensions, qty & prices
        - Joinery section
        - Furniture section
        - Payment terms & delivery terms
        - Arabic + English bilingual support
        - Footer with company info
    """,
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'depends': ['sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'report/quotation_report.xml',
        'report/quotation_report_template.xml',
        'views/sale_order_views.xml',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
