# -*- coding: utf-8 -*-
{
    'name': 'COA Sh Pdc',
    'summary': 'Post Dated Cheque Management, Manage Post Dated Cheque App, View Vendor Invoice PDC , List Of Customer PDC Payment, T...',
    'description': 'COA Sh Pdc developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.8.0.2.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.19.0.8.0.2',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['data/account_data.xml', 'data/ir_cron_cust.xml', 'data/mail_templates.xml', 'security/ir.model.access.csv', 'security/pdc_security.xml', 'wizard/pdc_payment_wizard_views.xml', 'wizard/pdc_multi_action_views.xml', 'views/account_move_views.xml', 'views/res_config_settings_views.xml', 'report/pdc_wizard_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
