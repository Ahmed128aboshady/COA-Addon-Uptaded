{
    'name': 'Sale Order Return',
    'version': '19.0.1.0.0',
    'summary': 'Create return transfers directly from sales orders',
    'category': 'Sales',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_return_wizard_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
