# -*- coding: utf-8 -*-
{
    'name': 'COA Mfg Location Routes',
    'summary': 'Enterprise-grade Mfg Location Routes solution for Odoo Inventory. Streamlines workflow execution, automates journal validations, and delivers real-time business insights.',
    'description': 'COA Mfg Location Routes developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '1.0.0',
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
