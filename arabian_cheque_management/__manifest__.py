# -*- coding: utf-8 -*-
{
    'name': 'arabian_cheque_management',
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': "\nLong description of module's purpose\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.0.1',
    'license': 'LGPL-3',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['base', 'accountant', 'account_accountant', 'utm'],
    'data': ['security/ir.model.access.csv', 'views/views.xml', 'views/templates.xml', 'wizard/check_accounts_cheque.xml', 'views/incoming_cheque.xml', 'views/outgoing_cheque.xml', 'views/res_config_settings.xml', 'views/account_move.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
