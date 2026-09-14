# -*- coding: utf-8 -*-
{
    'name': 'COA Partner Exact Reference Search',
    'version': '19.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Exact-match search on partner Reference (ref) in search bar and dropdowns',
    'description': """
COA Partner Exact Reference Search
==================================
Searching a partner by Reference (e.g. 538) with the default behaviour
also matches partners whose reference merely contains the digits
(e.g. 1538). This module adds:

* A "Reference (Exact)" search option in the partner search view
  that matches the reference exactly.
* An override of partner name_search so that typing a pure number in
  any partner dropdown (Sales Orders, Invoices, Payments, ...) first
  tries an exact match on the Reference field, falling back to the
  standard behaviour when no exact match exists.
""",
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
