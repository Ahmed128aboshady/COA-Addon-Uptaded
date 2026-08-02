# -*- coding: utf-8 -*-
{
    'name': 'COA Warehouse Stock Restrictions',
    'summary': 'Warehouse and Stock Location Restriction on Users.',
    'description': '\n        This Module Restricts the User from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'price': 25.0,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'sale', 'mrp'],
    'data': ['users_view.xml', 'security/security.xml', 'security/ir.model.access.csv'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
