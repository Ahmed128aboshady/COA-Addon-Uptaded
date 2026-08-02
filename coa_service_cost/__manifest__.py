# -*- coding: utf-8 -*-
{
    'name': 'COA Service Product Cost Flow',
    'summary': 'For service products: redirects purchase bills to an Intermediate Account (instead of expensing immediately), then on...',
    'description': '\nCOA Service Product Cost Flow\n==============================\n\nBusiness problem:\n-----------------\nStandard Odoo expenses service-product costs immediately on purchase\n(DR Expense / CR AP).  For project-based or resale services the cost\nshould only be recognised when the service is invoiced to the customer.\n\nSolution:\n---------\nConfigure two accounts on each service product (Accounting tab):\n\n  • Intermediate Account  – cost-in-transit buffer\n  • Cost of Sales Account – P&L account for the matched cost\n\nFlow:\n  1. Vendor bill posted  →  DR Intermediate / CR AP\n  2. Customer invoice posted → automatic journal entry:\n                                 DR Cost of Sales / CR Intermediate\n\nCredit-note reversals are handled symmetrically.\n\nDeveloped by Community of Accountants (COA)\nWhatsApp: +20 101 390 7174\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['account', 'product'],
    'data': ['views/product_template_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
