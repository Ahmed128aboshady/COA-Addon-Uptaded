{
    'name': 'Sale Stock Reserved',
    'version': '19.0.1.0.0',
    'summary': 'Report of reserved stock by customer and product from sales orders, with unreserve button',
    'category': 'Inventory/Reporting',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_stock_reserved_views.xml',
        'views/sale_stock_reserved_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
