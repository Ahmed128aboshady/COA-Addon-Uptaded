# -*- coding: utf-8 -*-
{
    'name': 'COA Mfg Location Routes',
    'summary': 'ربط لوكيشن السحب والتخزين بالكاتجوري تلقائياً في التصنيع والبيع والمرتجعات',
    'description': '\n        المشاكل اللي بيحلها المديول ده:\n        ====================================\n        1. ربط source location بالكاتجوري لكل عملية (تصنيع / بيع / مرتجع)\n        2. حل مشكلة "No rule has been found to replenish" للأصناف في sub-locations\n        3. إنشاء Stock Rules تلقائياً لكل كاتجوري عند الحفظ\n        4. دعم BUY + MTO مع لوكيشن مخصص\n        5. حقل لوكيشن على component في BOM يورث من الكاتجوري\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['stock', 'mrp', 'purchase', 'sale_stock', 'mrp_subcontracting'],
    'data': ['security/ir.model.access.csv', 'data/route_data.xml', 'views/product_category_views.xml', 'views/mrp_bom_views.xml', 'views/stock_rule_views.xml', 'wizard/wizard_fix_routes_views.xml', 'views/mfg_location_menu.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
