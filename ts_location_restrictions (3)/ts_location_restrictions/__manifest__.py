# -*- coding: utf-8 -*-
{
    'name': 'Warehouse Location & Operation Restriction',
    'version': '19.0.1.0.0',
    'summary': 'Restrict user access to specific warehouses, stock locations, and picking operation types with recursive permissions and validation guards.',
    'description': """
Warehouse Location & Operation Restriction for Odoo
==================================================
Secure your inventory management by limiting user access to specific warehouses, stock locations, and transfer picking operation types. Perfect for multi-warehouse companies and strict inventory audit compliance.

Key Features:
-------------
* **User-Level Restrictions Tab**: Easily configure restrictions directly on the User Form under a dedicated 'Location Restrictions' tab.
* **Warehouse Access Control**: Restrict inventory users so they can only view and select their designated warehouses.
* **Stock Location Restrictions**: Restrict access to specific locations (automatically includes all child stock locations recursively).
* **Operation Type Scope**: Limit user operations (e.g. only allow Receipt picking type, or restrict Internal Transfers).
* **Validation Security Guard**: Prevents validating, modifying, or viewing stock pickings, moves, and transfers involving unauthorized locations or operations, with clear and clean warning dialogs.
* **Stock Levels & Quant Filtering**: Automatically scopes inventory/stock quants view so users only see quantities in their allowed locations.
* **Odoo 19 Native Compatibility**: Rebuilt utilizing the Odoo 19 _search() hooks for optimal performance. Avoids legacy views and guards against admin bypass loop issues.

Protect your stock integrity and prevent unauthorized stock moves effortlessly.
    """,
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
    'category': 'Inventory/Warehouse',
    'license': 'AGPL-3',
    'depends': ['stock', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/stock_picking_views.xml',
    ],
    'price': 99.00,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/logo.png', 'static/description/icon.png'],
}
