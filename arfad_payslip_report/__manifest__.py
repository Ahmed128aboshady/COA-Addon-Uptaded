# -*- coding: utf-8 -*-
{
    'name': 'COA Arfad Payslip Report',
    'summary': 'Custom Bilingual Payslip Report Layout for Arfad',
    'description': 'COA Arfad Payslip Report developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Human Resources',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 39.0,
    'currency': 'EUR',
    'depends': ['hr_payroll', 'l10n_sa_hr_payroll'],
    'data': ['views/report_payslip_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
