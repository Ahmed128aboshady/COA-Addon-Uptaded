{
    'name': 'Product Secondary Unit of Measure',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Independent secondary UoM tracked alongside the primary UoM on products',
    'description': """
        Adds an independent secondary unit of measure on products.
        The secondary UoM is completely independent - no mathematical conversion
        between primary and secondary. Example: a product tracked as "2 Tons AND 3 Reels".
    """,
    'depends': [
        'product',
        'sale_stock',
        'purchase_stock',
        'stock',
        'mrp',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_move_views.xml',
        'views/stock_quant_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_bom_views.xml',
        'views/account_move_views.xml',
        'views/stock_product_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
