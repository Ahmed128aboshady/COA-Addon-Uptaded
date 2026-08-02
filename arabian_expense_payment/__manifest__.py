# -*- coding: utf-8 -*-
{
    'name': 'COA Arabian Expense Payment',
    'summary': "Short (1 phrase/line) summary of the module's purpose, used as         subtitle on modules listing or apps.openerp.com",
    'description': "\n        Long description of module's purpose\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
