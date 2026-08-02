# -*- coding: utf-8 -*-
{
    'name': 'COA Customer Portal Order',
    'summary': 'Empower customers to search products, select addresses, and request quotations.',
    'description': 'COA Customer Portal Order developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_management', 'portal', 'website'],
    'data': ['views/portal_templates.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
