# -*- coding: utf-8 -*-
{
    'name': 'COA Alramlaa Product Dimensions',
    'summary': 'Add Length, Width, Thickness, Square/Cubic Meter and Waste % to products',
    'description': 'COA Alramlaa Product Dimensions developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['product', 'purchase', 'stock', 'account_asset', 'mrp', 'base', 'account'],
    'data': ['security/ir.model.access.csv', 'data/company_migration_action.xml', 'views/product_template_views.xml', 'views/purchase_order_views.xml', 'views/stock_report_views.xml', 'views/mrp_views.xml', 'views/account_asset_views.xml', 'views/asset_category_views.xml', 'views/account_move_views.xml', 'views/report_invoice_custom.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
