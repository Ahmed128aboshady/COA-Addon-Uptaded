# -*- coding: utf-8 -*-
{
    'name': 'COA Quantity Available Warning',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Soft warning when the ordered quantity exceeds the free-to-use stock',
    'description': """
COA Quantity Available Warning
==============================
Shows a non-blocking warning when the requested quantity is greater than the
quantity available (Free To Use) across the whole company:

* Sale Order Line: an onchange warning appears while entering the quantity or
  the product, showing the available quantity. The user can still proceed.
* Delivery (stock.picking): on validation, a confirmation dialog lists the
  products short on stock. The user can press "Confirm Anyway" to continue.

Nothing is blocked - the warning is informative only.

Developed by Community of Accountants (COA) - Odoo Silver Partner
WhatsApp: +20 101 390 7174
    """,
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
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
