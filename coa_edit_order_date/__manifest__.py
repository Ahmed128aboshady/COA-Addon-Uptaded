# -*- coding: utf-8 -*-
{
    'name': 'Edit Sale Order Date',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Change the order date for particular user group',
    'description': 'We can change the order date of the confirmed sale order.The access for the editing the order date can berestricted to particular user group. The user who have no access to edit the field got a user error while trying tochange the field',
    'author': 'Community of Accountants',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.communityofaccountants.com',
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
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 19.0,
    'currency': 'USD',
}
