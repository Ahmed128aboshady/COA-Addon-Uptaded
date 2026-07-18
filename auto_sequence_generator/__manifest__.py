# -*- coding: utf-8 -*-
{
    'name': 'Auto Sequence Generator',
    'version': '19.0.1.0.0',
    'category': 'Technical',
    'summary': 'Auto-generate unique codes for products, customers, and vendors on record creation',
    'description': """
Auto Sequence Generator
========================
Automatically assigns unique reference codes when clicking the New button for:
- Products  → Internal Reference (PROD-0000001, PROD-0000002, ...)
- Customers → Customer Code    (CUST-0000001, CUST-0000002, ...)
- Vendors   → Vendor Code      (VEND-0000001, VEND-0000002, ...)

The generated code is displayed immediately and is read-only to prevent manual edits.
Sequences are fully configurable via Settings > Technical > Sequences.
    """,
    'author': 'Community of Accountants',
    'depends': [
        'product',
    ],
    'data': [
        'data/sequence_data.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
    'website': 'https://www.communityofaccountants.com',
    'price': 29.0,
    'currency': 'USD',
}
