# -*- coding: utf-8 -*-
{
    'name': 'COA Partial Quantity Relocate',
    'summary': 'Relocate a specific quantity (not the full quant) when using '
               'the Relocate action on stock locations / quants.',
    'description': """
COA Partial Quantity Relocate
=============================
The standard Odoo "Relocate" wizard (Inventory > Locations / Physical
Inventory) always moves the FULL on-hand quantity of each selected quant.

This module adds an editable line per selected quant inside the Relocate
wizard, so the user can specify exactly how much quantity to move to the
destination location. Lines left at 0 are skipped, lines at full quantity
follow the 100% native flow, and partial lines are moved using the same
native inventory-move mechanism (stock.move with is_inventory=True),
keeping lot / package / owner information intact.
    """,
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'author': 'Community of accountants (COA-Egypt)',
    'website': 'https://www.coa-egy.com',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_quant_relocate_views.xml',
    ],
    'installable': True,
    'application': False,
}
