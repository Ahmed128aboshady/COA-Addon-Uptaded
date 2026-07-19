# -*- coding: utf-8 -*-
{
    'description': """Balances sales security with flexible creation permissions:

Key Features:
* Restricts salespeople to viewing only their own orders (Own Documents group).
* Retains the ability to create new orders on behalf of other colleagues.
* Enhances collaborative selling without compromising pipeline privacy.""",
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Sale: Own View - Any Salesperson Create',
    'version': '18.0.1.0.0',
    'summary': 'Allow salesperson to create orders for any salesperson while restricted to own view.',
    'author': 'Community of Accountants (COA)',
    'category': 'Sales',
    'depends': [
        'sale',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'website': 'https://coa-egy.odoo.com/',
    'price': 25.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
