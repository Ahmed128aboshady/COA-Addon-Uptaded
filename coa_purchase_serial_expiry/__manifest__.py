# -*- coding: utf-8 -*-
{
    'name': 'COA Purchase Serial Expiry',
    'summary': 'Auto serial on PO/MO, expiry entry on receipts, FIFO auto-lot on delivery & MO',
    'description': 'COA Purchase Serial Expiry developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['purchase', 'mrp', 'stock', 'sale_stock', 'mail'],
    'data': ['security/ir.model.access.csv', 'data/ir_sequence_data.xml', 'data/ir_cron_data.xml', 'data/mail_template_data.xml', 'views/product_template_views.xml', 'views/purchase_order_views.xml', 'views/stock_picking_views.xml', 'views/mrp_production_views.xml', 'views/stock_lot_views.xml', 'views/stock_quant_views.xml', 'views/expiry_report_views.xml', 'views/menu_views.xml', 'report/expiry_report_template.xml', 'report/expiry_report_action.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
