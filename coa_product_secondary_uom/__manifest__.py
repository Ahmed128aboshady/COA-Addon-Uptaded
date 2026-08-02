# -*- coding: utf-8 -*-
{
    'name': 'COA Product Secondary Uom',
    'summary': 'Independent secondary UoM tracked alongside the primary UoM on products',
    'description': 'COA Product Secondary Uom developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['product', 'sale_stock', 'purchase_stock', 'stock', 'mrp', 'account'],
    'data': ['security/ir.model.access.csv', 'views/product_template_views.xml', 'views/sale_order_views.xml', 'views/purchase_order_views.xml', 'views/stock_picking_views.xml', 'views/stock_move_views.xml', 'views/stock_quant_views.xml', 'views/mrp_production_views.xml', 'views/mrp_bom_views.xml', 'views/account_move_views.xml', 'views/stock_product_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
