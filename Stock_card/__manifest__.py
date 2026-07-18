# -*- coding: utf-8 -*-
{
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
    'license': 'LGPL-3',
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
    'price': 69.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
