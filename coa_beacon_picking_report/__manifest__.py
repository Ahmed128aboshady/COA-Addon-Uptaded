# -*- coding: utf-8 -*-
{
    'name': 'COA Beacon Picking Report',
    'summary': 'Add sale order name under return reference in picking report',
    'description': 'COA Beacon Picking Report developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock', 'sale_stock'],
    'data': ['report/report_picking.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
