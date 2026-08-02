# -*- coding: utf-8 -*-
{
    'name': 'COA Qty Available Warning',
    'summary': 'Soft warning when the ordered quantity exceeds the free-to-use stock',
    'description': 'COA Qty Available Warning developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale_stock', 'stock'],
    'data': ['security/ir.model.access.csv', 'wizard/qty_warning_wizard_views.xml', 'views/sale_order_views.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
