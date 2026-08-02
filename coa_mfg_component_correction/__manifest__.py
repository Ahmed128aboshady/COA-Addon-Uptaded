# -*- coding: utf-8 -*-
{
    'name': 'COA Mfg Component Correction',
    'summary': 'Enterprise-grade Mfg Component Correction solution for Odoo Manufacturing. Streamlines workflow execution, automates journal validations, and delivers real-time business insights.',
    'description': 'COA Mfg Component Correction developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Manufacturing',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['mrp', 'stock', 'stock_account'],
    'data': ['security/ir.model.access.csv', 'wizard/mrp_component_correction_wizard_view.xml', 'views/mrp_production_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
