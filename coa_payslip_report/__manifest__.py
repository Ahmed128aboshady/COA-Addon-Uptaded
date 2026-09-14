{
    'name': 'Arfad Custom Payslip Report',
    'version': '19.0.1.0.0',
    'category': 'Payroll',
    'summary': 'Custom Bilingual Payslip Report Layout for Arfad',
    'description': """
        Replaces the default Odoo payslip PDF with a custom bilingual
        (Arabic / English) layout matching Arfad company design.
    """,
    'author': 'COA (Community of Accountants)',
    'depends': ['hr_payroll', 'l10n_sa_hr_payroll'],
    'data': [
        'views/report_payslip_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}