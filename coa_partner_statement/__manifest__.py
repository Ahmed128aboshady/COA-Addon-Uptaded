# -*- coding: utf-8 -*-
{
    'name': 'COA Partner Statement',
    'summary': 'Partner Account Statement Report with Opening Balance',
    'description': 'COA Partner Statement developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['security/ir.model.access.csv', 'wizard/partner_statement_wizard_views.xml', 'report/partner_statement_report.xml', 'report/partner_statement_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
