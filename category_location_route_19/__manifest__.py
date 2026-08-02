# -*- coding: utf-8 -*-
{
    'name': 'Category Location Route',
    'summary': 'Auto-create routes from product category location settings',
    'description': "\n        Add sales and manufacturing source locations to product categories.\n        The addon automatically creates/updates routes and procurement rules\n        so each product is pulled from its category's designated location.\n        Returns go back to the same source location automatically.\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock', 'sale_stock', 'mrp'],
    'data': ['security/ir.model.access.csv', 'views/product_category_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
