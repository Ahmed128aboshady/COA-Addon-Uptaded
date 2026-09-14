# -*- coding: utf-8 -*-
{
    'name': 'coa delegate_tracking',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Live location tracking and dashboard for sales delegates in the field.',
    'description': """
This module tracks the locations of sales delegates, updates their last known coordinates,
and displays their live and historical positions on an interactive OpenStreetMap map.
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'website': 'https://www.coa-egy.com',
    'depends': ['base', 'web', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/coa_delegate_views.xml',
        'views/delegate_location_views.xml',
        'views/delegate_visit_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
