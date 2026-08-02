# -*- coding: utf-8 -*-
{
    'name': 'Edit Sale Order Date',
    'summary': 'Allow specific user groups to edit the date of confirmed Sale Orders.',
    'description': 'Order Dates: Enables modifying the order date field even after sale orders are confirmed.\nAccess Control: Access is governed strictly by user groups and security permissions.\nSecurity Checks: Displays clear validation error messages to unauthorized users.\nScheduler Updates: Maintains full system integrity by updating corresponding scheduler entries.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale_management'],
    'data': ['security/coa_edit_order_date_groups.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
