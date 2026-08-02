# -*- coding: utf-8 -*-
{
    'name': 'COA Return Draft Invoice',
    'summary': 'When a warehouse return of a Sale Order is validated, the linked DRAFT customer invoice is automatically reduced by t...',
    'description': "\nCOA Adjust Draft Invoice on Stock Return\n========================================\nBusiness case:\n--------------\nA customer invoice is created in DRAFT (before posting). Later, some goods\nare returned from the warehouse against the same Sale Order. Standard Odoo\ndoes NOT sync the already-created draft invoice with the return, so the\ndraft still shows the old (higher) quantities.\n\nWhat this module does:\n----------------------\nOn validation of a return picking:\n  1. Detects the return moves (moves with origin_returned_move_id).\n  2. Finds the related Sale Order through the original delivery move.\n  3. Finds that order's DRAFT customer invoice(s).\n  4. Reduces the matching invoice line quantity by the returned quantity\n     (UoM-aware). Lines that reach zero are removed.\n  5. Logs a note in the invoice chatter for traceability.\n\nWhy draft only (audit trail safe):\n-----------------------------------\nThe module never modifies a POSTED invoice, so it fully respects the\nAccounting Audit Trail. For posted invoices the correct accounting action\nis a Credit Note (reversal) - available as an optional extension.\n\nNotes:\n------\n* The adjustment runs inside a guarded block: if anything fails, the\n  warehouse operation is NOT blocked (error is logged instead).\n* Trigger is narrow: only return moves linked to a Sale Order that has a\n  draft customer invoice.\n\nDeveloped by Community of Accountants (COA)\nWhatsApp: +20 101 390 7174\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '18.0.1.3.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_stock', 'account'],
    'data': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
