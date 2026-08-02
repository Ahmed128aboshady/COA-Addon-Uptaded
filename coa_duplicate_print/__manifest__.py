# -*- coding: utf-8 -*-
{
    'name': 'COA Duplicate Print Watermark',
    'summary': 'Show a DUPLICATE watermark when a document is re-printed',
    'description': '\nCOA Duplicate Print Watermark\n=============================\nCounts how many times a document has been printed to PDF and shows a big\nrotated "DUPLICATE - مكرر - Copy #N" watermark from the 2nd print onwards.\n\n* Supported documents: Sale Order / Quotation, Delivery Slip (stock.picking).\n* Configurable in General Settings: Disabled / Inventory only / Sales only /\n  Inventory and Sales.\n* The counter only increases on a real PDF print, not when opening the form.\n* Print info (count, date, user) is visible on the document form.\n* A "Reset Print Count" server action is available to treat the next print as\n  the original again.\n\nDeveloped by Community of Accountants (COA) - Odoo Silver Partner\nWhatsApp: +20 101 390 7174\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
