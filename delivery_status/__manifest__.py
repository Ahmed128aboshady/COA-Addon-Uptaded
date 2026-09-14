{
    'website': 'https://www.coa-egy.com',
    'name': 'Delivery Status in Sales Order',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Show delivery status in sales order form',
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['sale', 'sale_stock'],
    'data': [
        'views/sale_order_delivery_views.xml',
    ],
    'application': False,
    'auto_install': False,
}