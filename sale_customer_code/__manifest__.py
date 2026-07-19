# -*- coding: utf-8 -*-
{
    'description': """Document Codes: Automatically appends the customer's unique account code to printed documents.
Reports Supported: Appears on Sale Orders, Quotations, and Invoice PDFs.
Template Alignment: Clean styling integration matching standard Odoo document templates.""",
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
