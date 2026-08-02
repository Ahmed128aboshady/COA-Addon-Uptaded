# -*- coding: utf-8 -*-
{
    'name': 'COA Multi Approval',
    'summary': 'Multi-stage approval workflow for Sales, Purchase, Inventory and Accounting',
    'description': '\n        Configure multi-stage approval workflows for:\n        - Sale Orders (Quotations)\n        - Purchase Orders\n        - Vendor Bills / Customer Invoices (Accounting)\n        - Inventory Transfers (Stock Pickings)\n\n        Features:\n        - Unlimited configurable approval stages\n        - Per-stage approvers with flexible requirements (any/all/minimum)\n        - Automatic stage advancement\n        - Email & activity notifications\n        - Refuse with reason\n        - Auto-confirm option after full approval\n        - Full audit trail via chatter\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Project',
    'version': '17.0.19.0.1.2.0',
    'license': 'OPL-1',
    'price': 79.0,
    'currency': 'EUR',
    'depends': ['sale_management', 'purchase', 'account', 'stock', 'mail'],
    'data': ['security/multi_approval_security.xml', 'security/ir.model.access.csv', 'data/multi_approval_data.xml', 'wizard/approval_refuse_wizard_views.xml', 'views/multi_approval_type_views.xml', 'views/multi_approval_request_views.xml', 'views/sale_order_views.xml', 'views/purchase_order_views.xml', 'views/account_move_views.xml', 'views/account_payment_views.xml', 'views/stock_picking_views.xml', 'views/multi_approval_dashboard_views.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
