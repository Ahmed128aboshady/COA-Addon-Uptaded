{
    'website': 'https://www.coa-egy.com',
    'name': 'Arfad Custom Payslip Report',
    'version': '19.0.1.0.0',
    'category': 'Payroll',
    'summary': 'Custom Bilingual Payslip Report Layout for Arfad',
    'description': """
        Replaces the default Odoo payslip PDF with a custom bilingual
        (Arabic / English) layout matching Arfad company design.
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['hr', 'hr'],
    'data': [
        'views/report_payslip_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}