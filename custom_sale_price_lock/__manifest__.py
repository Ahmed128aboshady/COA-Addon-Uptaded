# -*- coding: utf-8 -*-
{
    'name': 'Custom Sale Price Lock',
    'summary': 'Lock sale order line unit price and allow editing for specific users only.',
    'description': 'Professional Custom Sale Price Lock custom module for Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Sales',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['sale_management'],
    'data': ['security/security.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
