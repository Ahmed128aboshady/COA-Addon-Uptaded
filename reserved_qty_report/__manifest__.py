{
    'website': 'https://www.coa-egy.com',
    'name': 'Reserved Qty Report',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Report showing reserved products in sales orders',
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['sale', 'stock', 'sale_stock'],
    'data': [
        'views/reserved_report_views.xml',
    ],
    'application': False,
    'auto_install': False,
}
