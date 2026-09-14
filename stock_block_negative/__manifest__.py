# -*- coding: utf-8 -*-
{
    "name": "Block Negative Stock",
    "summary": "Prevent stock levels from going negative anywhere in the system "
               "(manufacturing, deliveries, internal transfers, POS, adjustments via moves).",
    "version": "19.0.1.0.0",
    "category": "Inventory/Inventory",
    "author": "COA (Community of Accountants)",
    "license": "LGPL-3",
    "depends": ["stock"],
    "data": [
        "security/stock_block_negative_security.xml",
        "views/product_views.xml",
        "views/stock_location_views.xml",
    ],
    "installable": True,
    "application": False,
}
