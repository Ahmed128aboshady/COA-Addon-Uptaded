{
    'website': 'https://www.coa-egy.com',
    'author': 'Community of accountants (COA-Egypt)',
    'name': 'Stock Card Report',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Stock card report with running balance per product and location',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_card_wizard_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
