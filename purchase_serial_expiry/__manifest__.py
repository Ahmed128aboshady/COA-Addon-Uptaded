# -*- coding: utf-8 -*-
{
    'name': 'Purchase & Manufacturing Serial + Lot Expiry (FIFO)',
    'summary': 'Auto serial on PO/MO, expiry entry on receipts, FIFO auto-lot on delivery & MO',
    'description': '\n    Features\n    ========\n    1. Checkbox on product: "Requires Expiry Date on Purchase"\n       - Blocks receipt validation if expiry date is missing\n       - Auto-enables Lot tracking + FIFO removal strategy\n\n    2. Expiry Date entry on Receipt (Detailed Operations):\n       - Storekeeper fills Lot # + Expiry Date per line\n       - Multiple lines = multiple lots with different expiry dates\n       - Lots created automatically in stock on validation\n\n    3. FIFO auto-assignment on delivery (Sales) and Manufacturing:\n       - Detailed Operations auto-sorted: earliest expiry lot first\n       - MO raw material lines auto-filled with FIFO lots on produce\n\n    4. Auto serial number on Purchase Orders and Manufacturing Orders\n\n    5. Daily cron: email + chatter + activity 30 days before lot expiry\n\n    6. Lot Expiry Report (List / Graph / Pivot / PDF)\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['purchase', 'mrp', 'stock', 'sale_stock', 'mail'],
    'data': ['security/ir.model.access.csv', 'data/ir_sequence_data.xml', 'data/ir_cron_data.xml', 'data/mail_template_data.xml', 'views/product_template_views.xml', 'views/purchase_order_views.xml', 'views/stock_picking_views.xml', 'views/mrp_production_views.xml', 'views/stock_lot_views.xml', 'views/stock_quant_views.xml', 'views/expiry_report_views.xml', 'views/menu_views.xml', 'report/expiry_report_template.xml', 'report/expiry_report_action.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
