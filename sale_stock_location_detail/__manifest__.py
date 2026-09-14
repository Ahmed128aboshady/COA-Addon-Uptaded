{
    'name': 'Sale Line Reserved Location Detail',
    'version': '19.0.1.0.0',
    'summary': 'Show reserved sub-locations per SO line (from stock.move.line) in SO, invoice & print',
    'author': 'COA (Community of Accountants)',
    'depends': ['sale_stock', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'report/sale_order_report.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
