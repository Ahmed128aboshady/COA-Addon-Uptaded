# -*- coding: utf-8 -*-
{
    'name': 'COA Simplify Access Management',
    'summary': 'All In One Access Management App for setting the correct access rights for fields, models, menus, views for any modul...',
    'description': 'COA Simplify Access Management developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.2.1.8.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Extra Tools',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 79.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'web', 'coa_advanced_web_domain_widget'],
    'data': ['security/res_groups.xml', 'security/ir.model.access.csv', 'data/view_data.xml', 'views/access_management_view.xml', 'views/res_users_view.xml', 'views/store_model_nodes_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
