# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Operation Stages',
    'summary': 'مراحل عمليات على المنتج قبل التسليم - مخزن عمليات - داشبورد تتبع',
    'description': 'COA Sale Operation Stages developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_stock', 'stock'],
    'data': ['security/security.xml', 'security/ir.model.access.csv', 'data/warehouse_data.xml', 'data/stage_data.xml', 'views/operation_stage_views.xml', 'views/sale_operation_views.xml', 'views/sale_order_views.xml', 'views/dashboard_views.xml', 'views/menu_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
