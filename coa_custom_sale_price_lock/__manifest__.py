# -*- coding: utf-8 -*-
{
    'name': 'COA Custom Sale Price Lock',
    'summary': 'Lock sale order line unit price and allow editing for specific users only.',
    'description': 'COA Custom Sale Price Lock developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale_management'],
    'data': ['security/security.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
