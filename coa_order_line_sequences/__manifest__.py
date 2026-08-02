# -*- coding: utf-8 -*-
{
    'name': 'COA Order Line Sequences',
    'summary': 'Sequence numbers in order lines of sales,purchase and delivery.',
    'description': 'COA Order Line Sequences developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['base', 'sale_management', 'purchase', 'stock'],
    'data': ['views/sale_order_views.xml', 'views/purchase_order_views.xml', 'views/stock_picking_views.xml', 'views/sale_order_templates.xml', 'views/stock_picking_templates.xml', 'views/purchase_order_templates.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
