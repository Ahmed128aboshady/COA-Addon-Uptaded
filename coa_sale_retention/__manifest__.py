# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Retention',
    'summary': 'Customer retention/holdback on sales: configurable percentage and holding period per order, automatic split of the re...',
    'description': 'Professional Sales Retention Money custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '17.0.19.0.2.0.1',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['sale_stock', 'account'],
    'data': ['views/res_config_settings_views.xml', 'views/sale_order_views.xml', 'views/account_move_views.xml', 'views/retention_menu.xml', 'report/retention_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
