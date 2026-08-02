# -*- coding: utf-8 -*-
{
    'name': 'COA Edit Order Date',
    'summary': 'Change the order date for particular user group',
    'description': 'We can change the order date of the confirmed sale order.The access for the editing the order date can berestricted to particular user group. The user who have no access to edit the field got a user error while trying tochange the field',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale_management'],
    'data': ['security/edit_order_date_groups.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
