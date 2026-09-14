{
    'website': 'https://www.coa-egy.com',
    'name': 'Purchase & Manufacturing Serial + Lot Expiry (FIFO)',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Auto serial on PO/MO, expiry entry on receipts, FIFO auto-lot on delivery & MO',
    'description': """
    Features
    ========
    1. Checkbox on product: "Requires Expiry Date on Purchase"
       - Blocks receipt validation if expiry date is missing
       - Auto-enables Lot tracking + FIFO removal strategy

    2. Expiry Date entry on Receipt (Detailed Operations):
       - Storekeeper fills Lot # + Expiry Date per line
       - Multiple lines = multiple lots with different expiry dates
       - Lots created automatically in stock on validation

    3. FIFO auto-assignment on delivery (Sales) and Manufacturing:
       - Detailed Operations auto-sorted: earliest expiry lot first
       - MO raw material lines auto-filled with FIFO lots on produce

    4. Auto serial number on Purchase Orders and Manufacturing Orders

    5. Daily cron: email + chatter + activity 30 days before lot expiry

    6. Lot Expiry Report (List / Graph / Pivot / PDF)
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['purchase', 'mrp', 'stock', 'sale_stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/mrp_production_views.xml',
        'views/stock_lot_views.xml',
        'views/stock_quant_views.xml',
        'views/expiry_report_views.xml',
        'views/menu_views.xml',
        'report/expiry_report_template.xml',
        'report/expiry_report_action.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
