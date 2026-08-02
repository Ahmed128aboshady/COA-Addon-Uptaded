# -*- coding: utf-8 -*-
{
    'name': 'COA Arfad Purchase Report',
    'summary': 'Custom PDF layout for Purchase Orders',
    'description': '\n        Replaces the default Odoo Purchase Order PDF with a custom \n        layout matching Arfad company design.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
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
