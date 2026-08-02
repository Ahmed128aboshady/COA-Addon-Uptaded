# -*- coding: utf-8 -*-
{
    'name': 'COA Delegate Tracking',
    'summary': 'Live location tracking and dashboard for sales delegates in the field.',
    'description': 'COA Delegate Tracking developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base', 'web', 'sale'],
    'data': ['security/ir.model.access.csv', 'views/coa_delegate_views.xml', 'views/delegate_location_views.xml', 'views/delegate_visit_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
