# -*- coding: utf-8 -*-
{
    'name': 'Sale Operation Stages',
    'version': '18.0.1.0.0',
    'summary': 'مراحل عمليات على المنتج قبل التسليم - مخزن عمليات - داشبورد تتبع',
    'author': 'Community of Accountants',
    'category': 'Sales/Inventory',
    'depends': [
        'sale_stock',
        'stock',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/warehouse_data.xml',
        'data/stage_data.xml',
        'views/operation_stage_views.xml',
        'views/sale_operation_views.xml',
        'views/sale_order_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'website': 'https://www.communityofaccountants.com',
    'price': 89.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
