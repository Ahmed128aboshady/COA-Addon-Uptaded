# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Stock Card Report',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Stock card report with running balance per product and location',
    'depends': [
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_card_wizard_views.xml',
    ],
    'installable': True,
    'license': 'OPL-1',
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'price': 69.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
