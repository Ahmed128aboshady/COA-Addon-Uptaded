# -*- coding: utf-8 -*-
{
    'name': 'COA Arabian Expense Payment',
    'summary': 'Professional Arabian Expense Payment solution for Odoo Accounting. Streamlines business operations, automates workflow validati...',
    'description': 'COA Arabian Expense Payment developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.0.1.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.0.1',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['base', 'accountant', 'hr'],
    'data': ['security/ir.model.access.csv', 'views/views.xml', 'views/templates.xml', 'views/expense_payment.xml', 'views/account_move.xml', 'views/account_journal.xml', 'report/expense_payment.xml', 'report/expense_payment_template.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
