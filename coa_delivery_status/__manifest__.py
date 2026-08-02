# -*- coding: utf-8 -*-
{
    'name': 'COA Delivery Status',
    'summary': 'Show delivery status in sales order form',
    'description': 'COA Delivery Status developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['sale', 'sale_stock'],
    'data': ['views/sale_order_delivery_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
