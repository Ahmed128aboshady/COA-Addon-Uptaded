# -*- coding: utf-8 -*-
{
    'name': 'COA Ent Ohrms Loan',
    'summary': 'Manage Loan Requests',
    'description': 'COA Ent Ohrms Loan developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Human Resources',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 39.0,
    'currency': 'EUR',
    'depends': ['base', 'hr_payroll', 'hr', 'account'],
    'data': ['security/hr_loan_security.xml', 'security/ir.model.access.csv', 'data/ir_sequence_data.xml', 'data/hr_payroll_structure_data.xml', 'data/hr_salary_rule_data.xml', 'data/hr_payslip_input_type_data.xml', 'views/hr_employee_views.xml', 'views/hr_loan_views.xml', 'views/hr_payroll_structure_views.xml', 'views/hr_payslip_views.xml', 'views/hr_salary_rule_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
