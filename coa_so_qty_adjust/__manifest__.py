# -*- coding: utf-8 -*-
{
    'name': 'COA: Sales Order Quantity Adjust (Draft Pickings)',
    'version': '19.0.1.0.0',
    'summary': 'Decrease draft delivery quantities in place instead of '
               'creating a delivery + return when the SO quantity is reduced.',
    'description': """
COA - Sales Order Quantity Adjustment
=====================================

When a confirmed Sales Order line quantity is decreased, standard Odoo
creates a negative procurement which results in a return move, even if the
original delivery is still in **draft**.

This module intercepts that case: as long as the related delivery moves are
still not done (draft / confirmed / waiting / assigned), it reduces the
existing outgoing move quantity in place instead of generating a return.

Behaviour:

* Quantity decreased, picking still not delivered  -> existing move reduced.
* Quantity decreased below already-delivered qty    -> standard behaviour (return).
* Any part of the line already delivered (done)      -> standard behaviour (return).
* Quantity increased                                 -> standard behaviour (new procurement).
""",
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales/Sales',
    'license': 'LGPL-3',
    'depends': ['sale_stock'],
    'data': [],
    'installable': True,
    'application': False,
}
