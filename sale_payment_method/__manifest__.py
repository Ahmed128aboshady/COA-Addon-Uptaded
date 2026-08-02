# -*- coding: utf-8 -*-
{
    'name': 'Sale Payment Method',
    'summary': 'Add payment method tags on sales orders and invoices with reporting',
    'description': 'Professional Sale Payment Method custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '18.0.2.0.0',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['security/ir.model.access.csv', 'data/payment_method_data.xml', 'views/res_partner_views.xml', 'views/sale_order_views.xml', 'views/account_move_views.xml', 'views/report_views.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
