# -*- coding: utf-8 -*-
{
    'name': 'COA Accrued Expense',
    'summary': 'Recognize vendor bill expenses over a period as accrued expenses.',
    'description': 'COA Accrued Expense developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['data/ir_cron.xml', 'views/res_config_settings_views.xml', 'views/account_move_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
