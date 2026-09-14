# -*- coding: utf-8 -*-
{
    'website': 'https://www.coa-egy.com',
    'author': 'Community of accountants (COA-Egypt)',
    'name': 'Alramlaa VAT Invoice Report',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom bilingual VAT Invoice PDF for Sale Orders',
    'description': 'Professional bilingual (Arabic/English) VAT Invoice report for Sale Orders',
    'depends': ['sale_stock'],
    'data': [
        'report/ir_actions_report.xml',
        'report/sale_order_invoice_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
