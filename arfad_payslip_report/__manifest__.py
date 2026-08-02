# -*- coding: utf-8 -*-
{
    'name': 'COA Arfad Payslip Report',
    'summary': 'Custom Bilingual Payslip Report Layout for Arfad',
    'description': '\n        Replaces the default Odoo payslip PDF with a custom bilingual\n        (Arabic / English) layout matching Arfad company design.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
