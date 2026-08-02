# -*- coding: utf-8 -*-
{
    'name': 'COA Duplicate Print',
    'summary': 'Show a DUPLICATE watermark when a document is re-printed',
    'description': 'COA Duplicate Print developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['base_setup', 'sale', 'stock'],
    'data': ['report/coa_duplicate_print_templates.xml', 'views/res_config_settings_views.xml', 'views/sale_order_views.xml', 'views/stock_picking_views.xml', 'data/server_actions.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
