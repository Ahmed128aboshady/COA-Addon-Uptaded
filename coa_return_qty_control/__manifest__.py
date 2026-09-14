# -*- coding: utf-8 -*-
{
    'name': 'COA Return Quantity Control',
    'version': '19.0.1.0.0',
    'summary': "Block returning more than the delivered quantity and show "
               "returned / remaining quantities on the return wizard and picking",
    'author': 'COA (Community of Accountants)',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [
        'views/stock_return_picking_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}
