# -*- coding: utf-8 -*-
{
    'name': 'Beacon Picking Report',
    'version': '19.0.1.0.0',
    'author': 'COA (Community of Accountants)',
    'category': 'Inventory',
    'summary': 'Add sale order name under return reference in picking report',
    'depends': ['stock', 'sale_stock'],
    'data': [
        'report/report_picking.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
