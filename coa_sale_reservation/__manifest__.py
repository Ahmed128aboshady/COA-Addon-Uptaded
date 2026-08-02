# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Reservation',
    'summary': 'Reservation checkbox on Sales Orders routed to a dedicated "Reservation" operation type (no routes needed)',
    'description': 'COA Sale Reservation developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 18.0.1.0.1.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '18.0.1.0.1',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['views/sale_order_views.xml', 'views/stock_picking_views.xml', 'report/sale_order_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
