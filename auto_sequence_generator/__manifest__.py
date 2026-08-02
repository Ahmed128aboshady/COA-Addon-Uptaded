# -*- coding: utf-8 -*-
{
    'name': 'Auto Sequence Generator',
    'summary': 'Auto-generate unique codes for products, customers, and vendors on record creation',
    'description': '\nAuto Sequence Generator\n========================\nAutomatically assigns unique reference codes when clicking the New button for:\n- Products  → Internal Reference (PROD-0000001, PROD-0000002, ...)\n- Customers → Customer Code    (CUST-0000001, CUST-0000002, ...)\n- Vendors   → Vendor Code      (VEND-0000001, VEND-0000002, ...)\n\nThe generated code is displayed immediately and is read-only to prevent manual edits.\nSequences are fully configurable via Settings > Technical > Sequences.\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.2.2',
    'license': 'LGPL-3',
    'price': 15.0,
    'currency': 'EUR',
    'depends': ['product'],
    'data': ['data/sequence_data.xml', 'views/product_template_views.xml', 'views/res_partner_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
