# -*- coding: utf-8 -*-
{
    'name': 'COA Mfg Production Variance',
    'summary': 'Planned vs Produced quantity variance report for Manufacturing Orders',
    'description': 'COA Mfg Production Variance developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.2.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Manufacturing',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['mrp', 'sale_stock'],
    'data': ['security/ir.model.access.csv', 'views/production_variance_views.xml', 'wizard/production_variance_wizard_views.xml', 'report/production_variance_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
