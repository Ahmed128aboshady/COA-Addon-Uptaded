# -*- coding: utf-8 -*-
{
    'website': 'https://www.coa-egy.com',
    'name': 'Sales Commission by Customer Tag',
    'version': '19.0.1.0.0',
    'summary': 'Calculate sales commissions based on customer tag and net sales',
    'description': """
        Sales Commission Module
        ========================
        - Calculates commission from net sales (Invoice Analysis)
        - Rate is determined based on the customer tag
        - Tags and rates can be added and modified from the Settings
        - Comprehensive report for each salesperson
    """,
    'category': 'Sales/Commission',
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['sale_management', 'account', 'crm', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/commission_rate_views.xml',
        'views/commission_line_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/commission_analysis_wizard_views.xml',
        'wizard/commission_payment_wizard_views.xml',
        'views/menu_views.xml',
        'report/commission_report_template.xml',
        'report/commission_report_action.xml',
        'report/commission_analysis_template.xml',
        'report/commission_analysis_action.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
