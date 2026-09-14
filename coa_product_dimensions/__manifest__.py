# -*- coding: utf-8 -*-
{
    'name': 'Alramlaa Product Dimensions',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Products',
    'summary': 'Add Length, Width, Thickness, Square/Cubic Meter and Waste % to products',
    'depends': ['product', 'purchase', 'stock', 'account_asset', 'mrp', 'base', 'account'], # ضفنا mrp هنا
    'data': [
        'security/ir.model.access.csv',
        'data/company_migration_action.xml', # 👈 ضفنا مسار ملف الـ Server Action الجديد هنا
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_report_views.xml',
        'views/mrp_views.xml',
        'views/account_asset_views.xml',
        'views/asset_category_views.xml',
        'views/account_move_views.xml',
        'views/report_invoice_custom.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}