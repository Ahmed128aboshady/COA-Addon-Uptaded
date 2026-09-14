{
    'name': 'COA Service Product Cost Flow',
    'version': '19.0.1.0.0',
    'summary': (
        'For service products: redirects purchase bills to an Intermediate '
        'Account (instead of expensing immediately), then on customer invoice '
        'automatically creates a COGS ← Intermediate cost journal entry.'
    ),
    'description': """
COA Service Product Cost Flow
==============================

Business problem:
-----------------
Standard Odoo expenses service-product costs immediately on purchase
(DR Expense / CR AP).  For project-based or resale services the cost
should only be recognised when the service is invoiced to the customer.

Solution:
---------
Configure two accounts on each service product (Accounting tab):

  • Intermediate Account  – cost-in-transit buffer
  • Cost of Sales Account – P&L account for the matched cost

Flow:
  1. Vendor bill posted  →  DR Intermediate / CR AP
  2. Customer invoice posted → automatic journal entry:
                                 DR Cost of Sales / CR Intermediate

Credit-note reversals are handled symmetrically.

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['account', 'product'],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}
