# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Edit Sale Order Date',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Allow specific user groups to edit the date of confirmed Sale Orders.',
    'description': """Enables modifying the order date field even after sale orders are confirmed:

Key Features:
* Access is governed strictly by user groups and security permissions.
* Displays clear validation error messages to unauthorized users.
* Maintains full system integrity by updating corresponding scheduler entries.""""Enables modifying the order date field even after sale orders are confirmed:

Key Features:
* Access is governed strictly by user groups and security permissions.
* Displays clear validation error messages to unauthorized users.
* Maintains full system integrity by updating corresponding scheduler entries.""",
    'author': 'Community of Accountants (COA)',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://coa-egy.odoo.com/',
    'depends': [
        'sale_management',
    ],
    'data': [
        'security/coa_edit_order_date_groups.xml',
        'views/sale_order_views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 19.0,
    'currency': 'USD',
}
