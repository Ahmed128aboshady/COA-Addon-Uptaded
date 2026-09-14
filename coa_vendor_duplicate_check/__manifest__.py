# -*- coding: utf-8 -*-
{
    "name": "Vendor Duplicate Check (Email / Phone)",
    "version": "19.0.1.0.0",
    "category": "Contacts",
    "summary": "Warn or block when a vendor's email or phone is already used by another contact.",
    "description": """
Vendor Duplicate Check
======================

Odoo natively alerts on duplicate Tax ID / Company Registry when a vendor is
created (including by duplicating an existing vendor), but it does NOT check for
a duplicate Email or Phone number.

This module adds that check on ``res.partner``:

* On save it can **block** the record (ValidationError) or only **warn**.
* A live **on-change warning** flags duplicates while typing / after duplicating.
* Configurable from *Settings > Duplicate Check*:
    - Handling mode: Block save / Warn only
    - Scope: Vendors only / All contacts
    - Which fields to check: Email, Phone

Note (Odoo 19): the separate ``mobile`` field was removed from contacts and
merged into ``phone``, so the mobile number is validated through ``phone``.
""",
    "author": "COA (Community of Accountants)",
    "website": "https://www.coa-egy.com",
    "license": "LGPL-3",
    "depends": ["base_setup"],
    "data": [
        "data/ir_config_parameter.xml",
        "views/res_config_settings_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": False,
}
