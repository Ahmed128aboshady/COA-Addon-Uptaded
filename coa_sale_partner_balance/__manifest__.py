# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Partner Balance',
    'summary': 'Display partner previous and current balance on Sale Order and Invoice reports',
    'description': 'COA Sale Partner Balance developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.2.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.19.0.2.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['report/sale_report_templates.xml', 'report/invoice_report_templates.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
