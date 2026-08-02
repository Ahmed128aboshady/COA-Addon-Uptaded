# -*- coding: utf-8 -*-
{
    'name': 'COA Partial Relocate',
    'summary': 'Relocate a specific quantity (not the full quant) when using the Relocate action on stock locations / quants.',
    'description': '\nCOA Partial Quantity Relocate\n=============================\nThe standard Odoo "Relocate" wizard (Inventory > Locations / Physical\nInventory) always moves the FULL on-hand quantity of each selected quant.\n\nThis module adds an editable line per selected quant inside the Relocate\nwizard, so the user can specify exactly how much quantity to move to the\ndestination location. Lines left at 0 are skipped, lines at full quantity\nfollow the 100% native flow, and partial lines are moved using the same\nnative inventory-move mechanism (stock.move with is_inventory=True),\nkeeping lot / package / owner information intact.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': ['security/ir.model.access.csv', 'wizard/stock_quant_relocate_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
