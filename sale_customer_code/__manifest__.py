# -*- coding: utf-8 -*-
{
    'description': """Automatically appends the customer's unique account code to printed documents:

Key Features:
* Appears on Sale Orders, Quotations, and Invoice PDFs.
* Helps warehouses and billing teams quickly map paperwork.
* Clean styling integration matching standard Odoo document templates.""",
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Customer Code on Sale Order Report',
    'version': '18.0.1.0.0',
    'summary': 'Display the customer reference code on printed sale order and invoice reports.',
    'author': 'Community of Accountants (COA)',
    'category': 'Sales',
    'depends': [
        'sale',
    ],
    'data': [
        'report/sale_report_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
    'website': 'https://coa-egy.odoo.com/',
    'price': 15.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
