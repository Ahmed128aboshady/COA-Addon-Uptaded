# -*- coding: utf-8 -*-
{
    'name': 'COA Simplify Access Management V19',
    'summary': 'All In One Access Management App for setting the correct access rights for fields, models, menus, views for any modul...',
    'description': 'COA Simplify Access Management V19 developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.5.3.8.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '17.0.19.0.5.3.8',
    'license': 'OPL-1',
    'price': 79.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'web'],
    'data': ['security/res_groups.xml', 'security/ir.model.access.csv', 'data/view_data.xml', 'views/access_management_view.xml', 'views/res_users_view.xml', 'views/store_model_nodes_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
