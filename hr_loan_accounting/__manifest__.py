# -*- coding: utf-8 -*-
{
    'name': 'HR Loan Accounting',
    'summary': 'Accounting integration for HR Loans',
    'description': 'Adds journal entry creation on loan approval, smart button for journal entries, and installment delay wizard.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['ent_ohrms_loan', 'account'],
    'data': ['security/ir.model.access.csv', 'views/delay_installments_views.xml', 'views/hr_loan_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
