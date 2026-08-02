# -*- coding: utf-8 -*-
{
    'name': 'COA Partial Relocate',
    'summary': 'Relocate a specific quantity (not the full quant) when using the Relocate action on stock locations / quants.',
    'description': 'COA Partial Relocate developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['security/ir.model.access.csv', 'wizard/stock_quant_relocate_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
