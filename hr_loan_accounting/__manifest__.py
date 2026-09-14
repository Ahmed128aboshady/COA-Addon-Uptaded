{
    'name': 'HR Loan Accounting',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Accounting integration for HR Loans',
    'description': 'Adds journal entry creation on loan approval, '
                   'smart button for journal entries, and installment delay wizard.',
    'depends': ['ent_ohrms_loan', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/delay_installments_views.xml',
        'views/hr_loan_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
