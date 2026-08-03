# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Payment Method',
    'summary': 'Add payment method tags on sales orders and invoices with reporting',
    'description': 'COA Sale Payment Method developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.2.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['security/ir.model.access.csv', 'data/payment_method_data.xml', 'views/res_partner_views.xml', 'views/sale_order_views.xml', 'views/account_move_views.xml', 'views/report_views.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
