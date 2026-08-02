# -*- coding: utf-8 -*-
{
    'name': 'COA Vendor Duplicate Check',
    'summary': "Warn or block when a vendor's email or phone is already used by another contact.",
    'description': 'COA Vendor Duplicate Check developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base_setup'],
    'data': ['data/ir_config_parameter.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
