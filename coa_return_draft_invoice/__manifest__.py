# -*- coding: utf-8 -*-
{
    'name': 'COA Adjust Draft Invoice on Stock Return',
    'summary': 'When a warehouse return of a Sale Order is validated, the linked DRAFT customer invoice is automatically reduced by the returned quantities. Audit-trail safe (never touches posted entries).',
    'description': """
COA Adjust Draft Invoice on Stock Return
========================================
Business case:
--------------
A customer invoice is created in DRAFT (before posting). Later, some goods
are returned from the warehouse against the same Sale Order. Standard Odoo
does NOT sync the already-created draft invoice with the return, so the
draft still shows the old (higher) quantities.

What this module does:
----------------------
On validation of a return picking:
  1. Detects the return moves (moves with origin_returned_move_id).
  2. Finds the related Sale Order through the original delivery move.
  3. Finds that order's DRAFT customer invoice(s).
  4. Reduces the matching invoice line quantity by the returned quantity
     (UoM-aware). Lines that reach zero are removed.
  5. Logs a note in the invoice chatter for traceability.

Why draft only (audit trail safe):
-----------------------------------
The module never modifies a POSTED invoice, so it fully respects the
Accounting Audit Trail. For posted invoices the correct accounting action
is a Credit Note (reversal) - available as an optional extension.

Notes:
------
* The adjustment runs inside a guarded block: if anything fails, the
  warehouse operation is NOT blocked (error is logged instead).
* Trigger is narrow: only return moves linked to a Sale Order that has a
  draft customer invoice.

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    """,
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
    'category': 'Inventory/Sales',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'sale_stock',
        'account',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'price': 39.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
