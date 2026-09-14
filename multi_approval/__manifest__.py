{
    'website': 'https://www.coa-egy.com',
    'name': 'Multi Approval',
    'version': '19.0.1.0.0',
    'category': 'Approvals',
    'summary': 'Multi-stage approval workflow for Sales, Purchase, Inventory and Accounting',
    'description': """
        Configure multi-stage approval workflows for:
        - Sale Orders (Quotations)
        - Purchase Orders
        - Vendor Bills / Customer Invoices (Accounting)
        - Inventory Transfers (Stock Pickings)

        Features:
        - Unlimited configurable approval stages
        - Per-stage approvers with flexible requirements (any/all/minimum)
        - Automatic stage advancement
        - Email & activity notifications
        - Refuse with reason
        - Auto-confirm option after full approval
        - Full audit trail via chatter
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['sale_management', 'purchase', 'account', 'stock', 'mail'],
    'data': [
        'security/multi_approval_security.xml',
        'security/ir.model.access.csv',
        'data/multi_approval_data.xml',
        'wizard/approval_refuse_wizard_views.xml',
        'views/multi_approval_type_views.xml',
        'views/multi_approval_request_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'views/stock_picking_views.xml',
        'views/multi_approval_dashboard_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
