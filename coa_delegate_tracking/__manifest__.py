# -*- coding: utf-8 -*-
{
    'name': 'coa delegate_tracking',
    'summary': 'Live location tracking and dashboard for sales delegates in the field.',
    'description': '\nThis module tracks the locations of sales delegates, updates their last known coordinates,\nand displays their live and historical positions on an interactive OpenStreetMap map.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base', 'web', 'sale'],
    'data': ['security/ir.model.access.csv', 'views/coa_delegate_views.xml', 'views/delegate_location_views.xml', 'views/delegate_visit_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
