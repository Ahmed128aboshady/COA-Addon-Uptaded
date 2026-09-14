{
    'website': 'https://www.coa-egy.com',
    'name': 'Petty Cash Management',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Manage petty cash custodies and expenses with full accounting integration',
    'description': """
        Petty Cash Management System:
        - Each employee registers their own expenses
        - Accountants see all employee custodies and remaining balances
        - Each employee sees only their own expenses
        - Full accounting integration with automatic journal entries
        - Each category has a dedicated expense account
        - Custody account configured from Settings
        - Multi-level approval workflow
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['base', 'mail', 'hr', 'account'],
    'data': [
        'security/petty_cash_security.xml',
        'security/ir.model.access.csv',
        'views/petty_cash_config_views.xml',
        'views/petty_cash_approver_views.xml',
        'views/petty_cash_category_views.xml',
        'views/petty_cash_custody_views.xml',
        'views/petty_cash_expense_views.xml',
        'views/petty_cash_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
}
