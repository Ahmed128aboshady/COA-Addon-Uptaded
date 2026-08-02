# -*- coding: utf-8 -*-
{
    'name': 'COA Alramlaa Custom Hr Updates',
    'summary': 'Customizations for HR Units, Departments, and Kafala Status',
    'description': 'COA Alramlaa Custom Hr Updates developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Human Resources',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['base', 'hr'],
    'data': ['security/ir.model.access.csv', 'views/hr_custom_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
