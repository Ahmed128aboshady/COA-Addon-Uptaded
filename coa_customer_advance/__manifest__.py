# -*- coding: utf-8 -*-
{
    'name': 'COA Customer Advance',
    'summary': 'Enterprise-grade Customer Advance solution for Odoo Sales. Streamlines workflow execution, automates journal validations, and delivers real-time business insights.',
    'description': 'COA Customer Advance developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.1.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['account', 'sale_management'],
    'data': ['security/ir.model.access.csv', 'data/account_advance_data.xml', 'wizard/advance_settle_wizard_views.xml', 'views/account_payment_views.xml', 'views/account_move_views.xml', 'views/sale_advance_payment_inv_views.xml', 'views/sale_order_views.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
