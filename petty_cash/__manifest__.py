# -*- coding: utf-8 -*-
{
    'name': 'Petty Cash Management',
    'summary': 'Manage petty cash custodies and expenses with full accounting integration',
    'description': '\n        Petty Cash Management System:\n        - Each employee registers their own expenses\n        - Accountants see all employee custodies and remaining balances\n        - Each employee sees only their own expenses\n        - Full accounting integration with automatic journal entries\n        - Each category has a dedicated expense account\n        - Custody account configured from Settings\n        - Multi-level approval workflow\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.3.0.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'hr', 'account'],
    'data': ['security/petty_cash_security.xml', 'security/ir.model.access.csv', 'views/petty_cash_config_views.xml', 'views/petty_cash_approver_views.xml', 'views/petty_cash_category_views.xml', 'views/petty_cash_custody_views.xml', 'views/petty_cash_expense_views.xml', 'views/petty_cash_menu.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
