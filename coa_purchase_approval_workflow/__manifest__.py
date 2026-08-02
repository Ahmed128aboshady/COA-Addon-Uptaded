# -*- coding: utf-8 -*-
{
    'name': 'COA Purchase Approval Workflow',
    'summary': 'Configurable multi-level purchase order approval workflow',
    'description': 'COA Purchase Approval Workflow developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.4.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Project',
    'version': '17.0.19.0.4.0.0',
    'license': 'OPL-1',
    'price': 59.0,
    'currency': 'EUR',
    'depends': ['purchase', 'mail', 'hr'],
    'data': ['security/security_groups.xml', 'security/ir.model.access.csv', 'security/record_rules.xml', 'data/mail_template_data.xml', 'data/cron_data.xml', 'views/purchase_approval_matrix_diagram_views.xml', 'views/purchase_approval_matrix_views.xml', 'views/purchase_approval_history_views.xml', 'views/purchase_approval_reject_wizard_views.xml', 'views/purchase_order_views.xml', 'views/purchase_approval_dashboard_views.xml', 'views/res_users_views.xml', 'views/res_partner_views.xml', 'views/res_config_settings_views.xml', 'views/purchase_approval_analytics_views.xml', 'views/purchase_approval_policy_wizard_views.xml', 'views/purchase_approval_audit_export_wizard_views.xml', 'views/purchase_approval_audit_trail_report.xml', 'views/menu_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
