# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'COA Adjust Draft Invoice on Stock Return',
    'summary': 'Auto-reduce draft invoice quantities when warehouse returns are validated.',
    'description': """Keeps draft customer invoices fully synced with warehouse returns:

Key Features:
* On validating a stock return, automatically identifies related sale orders.
* Finds any associated draft customer invoices.
* Automatically reduces the draft invoice quantities by the returned amount.
* Fully audit-safe: never modifies posted invoices.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'category': 'Inventory/Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'depends': [
        'sale_stock',
        'account',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'price': 39.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
