# -*- coding: utf-8 -*-
{
    'name': "coa_expense_payment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Community of accountants (COA-Egypt)",
    'website': "https://www.coa-egy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/expense_payment.xml',
        'views/account_move.xml',
        'views/account_journal.xml',
        'report/expense_payment.xml',
        'report/expense_payment_template.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
