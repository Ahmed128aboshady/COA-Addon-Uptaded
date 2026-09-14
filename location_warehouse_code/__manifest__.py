{
    'website': 'https://www.coa-egy.com',
    'name': 'Location & Warehouse Code',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Configuration',
    'summary': 'Add code field to Location and Warehouse configuration',
    'description': """
        This module adds a 'Code' field after the 'Name' field in:
        - Stock Location configuration
        - Warehouse configuration
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['stock'],
    'data': [
        'views/stock_location_views.xml',
        'views/stock_warehouse_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
