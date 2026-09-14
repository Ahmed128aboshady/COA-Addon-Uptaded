# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing Location Routes (مسارات المخزون بالكاتجوري)',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'ربط لوكيشن السحب والتخزين بالكاتجوري تلقائياً في التصنيع والبيع والمرتجعات',
    'description': """
        المشاكل اللي بيحلها المديول ده:
        ====================================
        1. ربط source location بالكاتجوري لكل عملية (تصنيع / بيع / مرتجع)
        2. حل مشكلة "No rule has been found to replenish" للأصناف في sub-locations
        3. إنشاء Stock Rules تلقائياً لكل كاتجوري عند الحفظ
        4. دعم BUY + MTO مع لوكيشن مخصص
        5. حقل لوكيشن على component في BOM يورث من الكاتجوري
    """,
    'author': 'COA (Community of Accountants)',
    'depends': [
        'stock',
        'mrp',
        'purchase',
        'sale_stock',
        'mrp_subcontracting',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/route_data.xml',
        'views/product_category_views.xml',
        'views/mrp_bom_views.xml',
        'views/stock_rule_views.xml',
        'wizard/wizard_fix_routes_views.xml',
        'views/mfg_location_menu.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
