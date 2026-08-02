# -*- coding: utf-8 -*-
{
    'name': 'Alramlaa Product Dimensions',
    'summary': 'Add Length, Width, Thickness, Square/Cubic Meter and Waste % to products',
    'description': 'Professional Alramlaa Product Dimensions custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['product', 'purchase', 'stock', 'account_asset', 'mrp', 'base', 'account'],
    'data': ['security/ir.model.access.csv', 'data/company_migration_action.xml', 'views/product_template_views.xml', 'views/purchase_order_views.xml', 'views/stock_report_views.xml', 'views/mrp_views.xml', 'views/account_asset_views.xml', 'views/asset_category_views.xml', 'views/account_move_views.xml', 'views/report_invoice_custom.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
