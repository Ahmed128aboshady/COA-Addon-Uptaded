# -*- coding: utf-8 -*-
{
    'name': 'Vendor Duplicate Check (Email / Phone)',
    'summary': "Warn or block when a vendor's email or phone is already used by another contact.",
    'description': '\nVendor Duplicate Check\n======================\n\nOdoo natively alerts on duplicate Tax ID / Company Registry when a vendor is\ncreated (including by duplicating an existing vendor), but it does NOT check for\na duplicate Email or Phone number.\n\nThis module adds that check on ``res.partner``:\n\n* On save it can **block** the record (ValidationError) or only **warn**.\n* A live **on-change warning** flags duplicates while typing / after duplicating.\n* Configurable from *Settings > Duplicate Check*:\n    - Handling mode: Block save / Warn only\n    - Scope: Vendors only / All contacts\n    - Which fields to check: Email, Phone\n\nNote (Odoo 19): the separate ``mobile`` field was removed from contacts and\nmerged into ``phone``, so the mobile number is validated through ``phone``.\n',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['base_setup'],
    'data': ['data/ir_config_parameter.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
