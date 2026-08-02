# -*- coding: utf-8 -*-
{
    'name': 'COA Petty Cash',
    'summary': 'Manage petty cash custodies and expenses with full accounting integration',
    'description': 'COA Petty Cash developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.3.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.3.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'hr', 'account'],
    'data': ['security/petty_cash_security.xml', 'security/ir.model.access.csv', 'views/petty_cash_config_views.xml', 'views/petty_cash_approver_views.xml', 'views/petty_cash_category_views.xml', 'views/petty_cash_custody_views.xml', 'views/petty_cash_expense_views.xml', 'views/petty_cash_menu.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
