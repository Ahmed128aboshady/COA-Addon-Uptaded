# -*- coding: utf-8 -*-
{
    'name': 'COA Multi Approval',
    'summary': 'Multi-stage approval workflow for Sales, Purchase, Inventory and Accounting',
    'description': 'COA Multi Approval developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.2.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
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
