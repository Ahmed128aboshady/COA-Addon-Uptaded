# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Duplicate Print Watermark',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Show a DUPLICATE watermark automatically when a document is re-printed.',
    'description': """Tracks document printing counts and applies watermarks:

Key Features:
* Automatically prints a "DUPLICATE" watermark starting from the second print.
* Supported documents include Sale Orders, Quotations, and Delivery Slips.
* Configurable settings to enable/disable for Sales, Inventory, or both.
* Displays print logs including printer user, count, and date.
* Includes a "Reset Print Count" action for managers.""""Tracks document printing counts and applies watermarks:

Key Features:
* Automatically prints a "DUPLICATE" watermark starting from the second print.
* Supported documents include Sale Orders, Quotations, and Delivery Slips.
* Configurable settings to enable/disable for Sales, Inventory, or both.
* Displays print logs including printer user, count, and date.
* Includes a "Reset Print Count" action for managers.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'OPL-1',
    'depends': [
        'base_setup',
        'sale',
        'stock',
    ],
    'data': [
        'report/coa_duplicate_print_templates.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'data/server_actions.xml',
    ],
    'installable': True,
    'application': False,
    'price': 39.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
