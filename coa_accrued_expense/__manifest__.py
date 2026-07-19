# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Accrued Expenses',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Recognize vendor bill expenses over a period as accrued expenses.',
    'description': """
COA Accrued Expenses
====================
Mirrors Odoo's Deferred Expense mechanism, but as a separate *Accrued Expense*
feature:

* Choose a dedicated **Accrued Expense Account** and **Journal** in Settings.
* On a vendor bill line, tick **Accrued** and set a **Start** and **End** date.
* On posting the bill, the module moves the expense into the accrued account and
  then recognizes it month by month back into the expense account.
    """,
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'OPL-1',
    'depends': [
        'account',
    ],
    'data': [
        'data/ir_cron.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 59.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
