# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Reservation Operation',
    'summary': 'Reservation checkbox on Sales Orders routed to a dedicated "Reservation" operation type (no routes needed)',
    'description': '\nSale Reservation Operation\n==========================\nAdds an "is Reservation" checkbox on the Sales Order. When checked, the\ndelivery generated on confirmation is created under a dedicated outgoing\noperation type "حجز / Reservation" (own sequence RES/xxxxx, own card on\nthe Inventory Overview) instead of the standard Delivery type.\n\n* No routes, no internal transfers — same flow as a normal delivery.\n* The reservation picking type is created automatically per warehouse\n  the first time it is needed.\n* Stock is force-reserved on order confirmation, so reserved goods\n  cannot be taken by other orders.\n* Delivered quantities, invoicing and returns behave exactly like a\n  standard delivery.\n* Ready-made filters on Sales Orders and Transfers to isolate\n  reservations.\n\nBuilt for Odoo 18 (Community & Enterprise).\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '18.0.1.0.1',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': ['views/sale_order_views.xml', 'views/stock_picking_views.xml', 'report/sale_order_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
