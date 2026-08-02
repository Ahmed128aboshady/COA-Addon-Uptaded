# -*- coding: utf-8 -*-
{
    'name': 'COA So Tracking',
    'summary': 'متابعة أوامر البيع: كميات التصنيع والتسليم والفوترة لكل صنف',
    'description': 'COA So Tracking developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.1.1.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.1.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['sale', 'mrp', 'sale_mrp'],
    'data': ['views/so_tracking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
