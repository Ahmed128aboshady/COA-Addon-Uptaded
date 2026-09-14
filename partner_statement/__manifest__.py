{
    'website': 'https://www.coa-egy.com',
    'name': 'Partner Statement Report',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Partner Account Statement Report with Opening Balance',
    'description': """
        Generates a partner account statement report showing:
        - Opening balance before the selected period
        - All debit/credit transactions within the period
        - Running balance per line
        - Totals at the bottom
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/partner_statement_wizard_views.xml',
        'report/partner_statement_report.xml',
        'report/partner_statement_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
