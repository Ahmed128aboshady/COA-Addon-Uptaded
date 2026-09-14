{
    'website': 'https://www.coa-egy.com',
    'author': 'Community of accountants (COA-Egypt)',
    'name': 'Payment Status on Delivery',
    'version': '19.0.1.0.0',
    'summary': 'Shows invoice payment status automatically on delivery orders',
    'category': 'Inventory',
    'depends': [
        'sale_stock',
        'purchase_stock',
        'account',
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
