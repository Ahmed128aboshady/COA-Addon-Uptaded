{
    'name': 'Arfad HR Allowances',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Add 5 allowance fields to employee form',
    'depends': ['hr', 'hr_payroll', 'l10n_sa_hr_payroll'],
    'data': [
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'application': False,
}