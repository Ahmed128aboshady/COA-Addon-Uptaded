{
    'website': 'https://www.coa-egy.com',
    'name': 'Category Location Route',
    'version': '19.0.1.0.0',
    'summary': 'Auto-create routes from product category location settings',
    'description': """
        Add sales and manufacturing source locations to product categories.
        The addon automatically creates/updates routes and procurement rules
        so each product is pulled from its category's designated location.
        Returns go back to the same source location automatically.
    """,
    'category': 'Inventory',
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['stock', 'sale_stock', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
