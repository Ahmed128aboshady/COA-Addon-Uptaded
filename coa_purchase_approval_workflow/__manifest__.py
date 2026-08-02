# -*- coding: utf-8 -*-
{
    'name': 'COA Purchase Approval Workflow',
    'summary': 'Configurable multi-level purchase order approval workflow',
    'description': "\nPurchase Approval Workflow\n==========================\nIntroduces a fully configurable, multi-level purchase order approval workflow\nwith 14 advanced features for enterprise-grade procurement governance.\n\nKey Features:\n1.  SLA & Escalation: per-level deadline, overdue badge, automatic escalation cron\n2.  One-Click Email Approval: tokenized Approve/Reject buttons in notification emails\n3.  Bulk Approval Dashboard: My/All Pending Approvals with inline actions and bulk server action\n4.  Delegation / Out-of-Office: delegate approvals to another user with an optional end date\n5.  Trusted Vendor Bypass: skip workflow for trusted vendors below a configurable amount limit\n6.  Parallel Approval (AND logic): require all group members to approve before advancing\n7.  HR Manager Auto-Routing: automatically route to the buyer's HR manager hierarchy\n8.  Budget Check Integration: real-time remaining budget warning on PO approval screen\n9.  Approval Analytics Dashboard: pivot + bar/trend graph views on approval history\n10. Change Summary on Resubmission: automatic chatter diff of what changed since last submission\n11. Approval Policy Templates: wizard to create pre-built matrix configurations in one click\n12. Vendor-Specific Rules: restrict matrix rules to a specific vendor\n13. Urgency Override: mark POs as Urgent or Critical to fast-track or escalate routing\n14. Export Audit Trail: download the full audit trail as a formatted Excel file or branded PDF\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
