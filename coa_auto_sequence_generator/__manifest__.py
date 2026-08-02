# -*- coding: utf-8 -*-
{
    'name': 'COA Auto Sequence Generator',
    'summary': 'Auto-generate unique codes for products, customers, and vendors on record creation',
    'description': 'COA Auto Sequence Generator developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.2.2.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.2.2',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['product'],
    'data': ['data/sequence_data.xml', 'views/product_template_views.xml', 'views/res_partner_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
