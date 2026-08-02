# -*- coding: utf-8 -*-
{
    'name': 'Partner Statement Report',
    'summary': 'Partner Account Statement Report with Opening Balance',
    'description': '\n        Generates a partner account statement report showing:\n        - Opening balance before the selected period\n        - All debit/credit transactions within the period\n        - Running balance per line\n        - Totals at the bottom\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['security/ir.model.access.csv', 'wizard/partner_statement_wizard_views.xml', 'report/partner_statement_report.xml', 'report/partner_statement_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
