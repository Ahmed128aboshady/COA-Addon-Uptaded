{
    'name': 'Custom Sale Price Lock',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Lock sale order line unit price and allow editing for specific users only.',
    'depends': ['sale_management'],
    'data': [
        'security/security.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}