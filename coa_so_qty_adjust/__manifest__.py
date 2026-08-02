# -*- coding: utf-8 -*-
{
    'name': 'COA So Qty Adjust',
    'summary': 'Decrease draft delivery quantities in place instead of creating a delivery + return when the SO quantity is reduced.',
    'description': '\nCOA - Sales Order Quantity Adjustment\n=====================================\n\nWhen a confirmed Sales Order line quantity is decreased, standard Odoo\ncreates a negative procurement which results in a return move, even if the\noriginal delivery is still in **draft**.\n\nThis module intercepts that case: as long as the related delivery moves are\nstill not done (draft / confirmed / waiting / assigned), it reduces the\nexisting outgoing move quantity in place instead of generating a return.\n\nBehaviour:\n\n* Quantity decreased, picking still not delivered  -> existing move reduced.\n* Quantity decreased below already-delivered qty    -> standard behaviour (return).\n* Any part of the line already delivered (done)      -> standard behaviour (return).\n* Quantity increased                                 -> standard behaviour (new procurement).\n',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['sale_stock'],
    'data': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
