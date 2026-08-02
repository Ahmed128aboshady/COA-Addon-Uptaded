# -*- coding: utf-8 -*-
{
    'name': 'COA Account Restricted Access',
    'summary': 'Enterprise-grade Account Restricted Access solution for Odoo Accounting. Streamlines workflow execution, automates journal validations, and delivers real-time business insights.',
    'description': 'COA Account Restricted Access developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['security/account_restricted_security.xml', 'security/account_restricted_rules.xml', 'security/ir.model.access.csv', 'views/res_users_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
