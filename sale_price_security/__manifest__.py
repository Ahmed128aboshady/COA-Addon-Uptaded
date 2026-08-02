# -*- coding: utf-8 -*-
{
    'name': 'Sale Price Edit Permission',
    'summary': 'Add a checkbox permission to control who can edit sale order prices',
    'description': '\nAdds a new group "Can Edit Sale Prices" that appears as a checkbox\nin the user access rights page under the Sales section.\n\nWhen a user does NOT have this permission, the Unit Price field\nin sale order lines becomes read-only for them.\n\nBy default the group is granted to:\n- Administrators\n- Sales / Administrator (Sales Manager)\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_management'],
    'data': ['security/groups.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
