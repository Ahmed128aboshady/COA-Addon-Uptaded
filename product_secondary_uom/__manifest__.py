# -*- coding: utf-8 -*-
{
    'name': 'Product Secondary Unit of Measure',
    'summary': 'Independent secondary UoM tracked alongside the primary UoM on products',
    'description': '\n        Adds an independent secondary unit of measure on products.\n        The secondary UoM is completely independent - no mathematical conversion\n        between primary and secondary. Example: a product tracked as "2 Tons AND 3 Reels".\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['product', 'sale_stock', 'purchase_stock', 'stock', 'mrp', 'account'],
    'data': ['security/ir.model.access.csv', 'views/product_template_views.xml', 'views/sale_order_views.xml', 'views/purchase_order_views.xml', 'views/stock_picking_views.xml', 'views/stock_move_views.xml', 'views/stock_quant_views.xml', 'views/mrp_production_views.xml', 'views/mrp_bom_views.xml', 'views/account_move_views.xml', 'views/stock_product_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
