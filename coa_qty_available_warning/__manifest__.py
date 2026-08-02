# -*- coding: utf-8 -*-
{
    'name': 'COA Qty Available Warning',
    'summary': 'Soft warning when the ordered quantity exceeds the free-to-use stock',
    'description': '\nCOA Quantity Available Warning\n==============================\nShows a non-blocking warning when the requested quantity is greater than the\nquantity available (Free To Use) across the whole company:\n\n* Sale Order Line: an onchange warning appears while entering the quantity or\n  the product, showing the available quantity. The user can still proceed.\n* Delivery (stock.picking): on validation, a confirmation dialog lists the\n  products short on stock. The user can press "Confirm Anyway" to continue.\n\nNothing is blocked - the warning is informative only.\n\nDeveloped by Community of Accountants (COA) - Odoo Silver Partner\nWhatsApp: +20 101 390 7174\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
