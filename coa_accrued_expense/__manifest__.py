# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Accrued Expenses',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Recognize vendor bill expenses over a period as accrued expenses.',
    'description': """This module replicates deferred expense mechanics specifically for accrued expenses:

Key Features:
* Define custom accrued expense accounts and journals in Odoo Settings.
* Flag vendor bill lines as "Accrued" and specify start/end dates.
* Automatically creates reclassification entries moving expense to accrued account.
* Periodically recognizes the expense month by month.""""This module replicates deferred expense mechanics specifically for accrued expenses:

Key Features:
* Define custom accrued expense accounts and journals in Odoo Settings.
* Flag vendor bill lines as "Accrued" and specify start/end dates.
* Automatically creates reclassification entries moving expense to accrued account.
* Periodically recognizes the expense month by month.""",
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
