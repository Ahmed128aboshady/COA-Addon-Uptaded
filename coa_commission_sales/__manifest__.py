# -*- coding: utf-8 -*-
{
    'name': 'COA Commission Sales',
    'summary': 'Calculate sales commissions based on customer tag and net sales',
    'description': '\n        Sales Commission Module\n        ========================\n        - Calculates commission from net sales (Invoice Analysis)\n        - Rate is determined based on the customer tag\n        - Tags and rates can be added and modified from the Settings\n        - Comprehensive report for each salesperson\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['sale_management', 'account', 'crm', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/record_rules.xml', 'views/commission_rate_views.xml', 'views/commission_line_views.xml', 'views/res_config_settings_views.xml', 'wizard/commission_analysis_wizard_views.xml', 'wizard/commission_payment_wizard_views.xml', 'views/menu_views.xml', 'report/commission_report_template.xml', 'report/commission_report_action.xml', 'report/commission_analysis_template.xml', 'report/commission_analysis_action.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
