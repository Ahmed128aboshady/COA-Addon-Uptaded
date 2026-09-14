{
    'name': 'Custom Date Order',
    'author': 'COA (Community of Accountants)',
    'version': '19.0.1.0.0',

    'depends': ['sale', 'purchase'],
    'data': [
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
