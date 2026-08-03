# -*- coding: utf-8 -*-
{
    'name': 'COA Arabian Cheque Management',
    'summary': 'Professional Arabian Cheque Management solution for Odoo Accounting. Streamlines business operations, automates workflow valida...',
    'description': 'COA Arabian Cheque Management developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.0.1.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['base', 'accountant', 'account_accountant', 'utm'],
    'data': ['security/ir.model.access.csv', 'views/views.xml', 'views/templates.xml', 'wizard/check_accounts_cheque.xml', 'views/incoming_cheque.xml', 'views/outgoing_cheque.xml', 'views/res_config_settings.xml', 'views/account_move.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
