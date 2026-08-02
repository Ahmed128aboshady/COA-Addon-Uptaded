# -*- coding: utf-8 -*-
{
    'name': 'COA Partner Ref Exact Search',
    'summary': 'Exact-match search on partner Reference (ref) in search bar and dropdowns',
    'description': '\nCOA Partner Exact Reference Search\n==================================\nSearching a partner by Reference (e.g. 538) with the default behaviour\nalso matches partners whose reference merely contains the digits\n(e.g. 1538). This module adds:\n\n* A "Reference (Exact)" search option in the partner search view\n  that matches the reference exactly.\n* An override of partner name_search so that typing a pure number in\n  any partner dropdown (Sales Orders, Invoices, Payments, ...) first\n  tries an exact match on the Reference field, falling back to the\n  standard behaviour when no exact match exists.\n',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base'],
    'data': ['views/res_partner_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
