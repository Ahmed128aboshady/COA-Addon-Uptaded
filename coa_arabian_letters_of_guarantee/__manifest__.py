# -*- coding: utf-8 -*-
{
    'name': 'COA Arabian Letters Of Guarantee',
    'summary': 'Professional Arabian Letters Of Guarantee solution for Odoo Accounting. Streamlines business operations, automates workflow val...',
    'description': 'COA Arabian Letters Of Guarantee developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.0.1.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.0.1',
    'license': 'OPL-1',
    'price': 79.0,
    'currency': 'EUR',
    'depends': ['base', 'account', 'account_asset'],
    'data': ['security/ir.model.access.csv', 'views/views.xml', 'views/templates.xml', 'views/bid_bond.xml', 'views/performance_bond.xml', 'views/advance_payment_guarantee.xml', 'views/res_config_settings.xml', 'views/maintenance_bond.xml', 'views/account_move.xml', 'wizard/check_lg_accounts.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
