# -*- coding: utf-8 -*-
{
    'name': 'COA Commission Sales',
    'summary': 'Calculate sales commissions based on customer tag and net sales',
    'description': 'COA Commission Sales developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
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
