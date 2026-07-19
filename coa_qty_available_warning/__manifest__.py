# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Quantity Available Warning',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Soft warning when the ordered quantity exceeds available free-to-use stock.',
    'description': """Sale Warnings: Onchange warning triggers on Sale Order line when typing quantity.
Delivery Guards: Interactive validation dialog triggers on Delivery validation listing stock shortage.
Soft Warnings: Warnings are informative only — users can bypass and proceed.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'OPL-1',
    'depends': [
        'sale_stock',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/qty_warning_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'price': 29.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
