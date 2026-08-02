# -*- coding: utf-8 -*-
{
    'name': 'COA Category Location Route 19',
    'summary': 'Auto-create routes from product category location settings',
    'description': 'COA Category Location Route 19 developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock', 'sale_stock', 'mrp'],
    'data': ['security/ir.model.access.csv', 'views/product_category_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
