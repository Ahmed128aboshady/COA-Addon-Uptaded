# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Price Security',
    'summary': 'Add a checkbox permission to control who can edit sale order prices',
    'description': 'COA Sale Price Security developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_management'],
    'data': ['security/groups.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
