# -*- coding: utf-8 -*-
{
    'name': 'COA Hr Loan Accounting',
    'summary': 'Accounting integration for HR Loans',
    'description': 'COA Hr Loan Accounting developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['coa_ent_ohrms_loan', 'account'],
    'data': ['security/ir.model.access.csv', 'views/delay_installments_views.xml', 'views/hr_loan_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
