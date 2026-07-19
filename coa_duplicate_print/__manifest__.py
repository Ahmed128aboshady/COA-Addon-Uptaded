# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Duplicate Print Watermark',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Show a DUPLICATE watermark automatically when a document is re-printed.',
    'description': """
COA Duplicate Print Watermark
=============================
Counts how many times a document has been printed to PDF and shows a big
rotated "DUPLICATE - مكرر - Copy #N" watermark from the 2nd print onwards.

* Supported documents: Sale Order / Quotation, Delivery Slip (stock.picking).
* Configurable in General Settings: Disabled / Inventory only / Sales only /
  Inventory and Sales.
* The counter only increases on a real PDF print, not when opening the form.
* Print info (count, date, user) is visible on the document form.
* A "Reset Print Count" server action is available to treat the next print as
  the original again.

Developed by Community of Accountants (COA) - Odoo Silver Partner
WhatsApp: +20 101 390 7174
    """,
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
