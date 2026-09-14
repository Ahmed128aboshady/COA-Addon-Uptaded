# -*- coding: utf-8 -*-
{
    'name': "arabian_cheque_management",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "COA (Community of Accountants)",
    'website': "https://www.coa-egy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','accountant','account_accountant','utm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/check_accounts_cheque.xml',
        'views/incoming_cheque.xml',
        'views/outgoing_cheque.xml',
        'views/res_config_settings.xml',
        'views/account_move.xml',
        'views/menus.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

