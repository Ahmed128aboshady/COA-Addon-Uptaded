# -*- coding: utf-8 -*-
{
    'name': 'COA Arfad Purchase Report',
    'summary': 'Custom PDF layout for Purchase Orders',
    'description': 'COA Arfad Purchase Report developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['purchase'],
    'data': ['views/report_purchaseorder_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
