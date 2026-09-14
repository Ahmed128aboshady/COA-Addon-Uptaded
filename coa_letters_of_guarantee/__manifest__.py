# -*- coding: utf-8 -*-
{
    'name': "coa_letters_of_guarantee",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Community of accountants (COA-Egypt)",
    'website': "https://www.coa-egy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/bid_bond.xml',
        'views/performance_bond.xml',
        'views/advance_payment_guarantee.xml',
        'views/res_config_settings.xml',
        'views/maintenance_bond.xml',
        'views/account_move.xml',
        'wizard/check_lg_accounts.xml',
        'views/menus.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

