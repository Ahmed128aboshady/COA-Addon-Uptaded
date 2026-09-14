# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Reservation Operation',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Reservation checkbox on Sales Orders routed to a dedicated '
               '"Reservation" operation type (no routes needed)',
    'description': """
Sale Reservation Operation
==========================
Adds an "is Reservation" checkbox on the Sales Order. When checked, the
delivery generated on confirmation is created under a dedicated outgoing
operation type "حجز / Reservation" (own sequence RES/xxxxx, own card on
the Inventory Overview) instead of the standard Delivery type.

* No routes, no internal transfers — same flow as a normal delivery.
* The reservation picking type is created automatically per warehouse
  the first time it is needed.
* Stock is force-reserved on order confirmation, so reserved goods
  cannot be taken by other orders.
* Delivered quantities, invoicing and returns behave exactly like a
  standard delivery.
* Ready-made filters on Sales Orders and Transfers to isolate
  reservations.

Built for Odoo 18 (Community & Enterprise).
    """,
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'license': 'LGPL-3',
    'depends': ['sale_stock'],
    'data': [
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'report/sale_order_report.xml',
    ],
    'installable': True,
    'application': False,
}
