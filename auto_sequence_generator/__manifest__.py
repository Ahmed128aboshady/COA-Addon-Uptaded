# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Auto Sequence Generator',
    'version': '19.0.1.0.0',
    'category': 'Technical',
    'summary': 'Auto-generate unique codes for products, customers, and vendors on record creation.',
    'description': """Product Codes: Automatically generates Internal References (e.g. PROD-00001).
Customer Codes: Generates Customer Codes (e.g. CUST-00001).
Vendor Codes: Generates Vendor Codes (e.g. VEND-00001).
Technical Sequences: Easily edit sequences under Settings > Technical > Sequences.
Read-Only Protection: Protects auto-generated reference fields from unauthorized edits.""",
    'author': 'Community of Accountants (COA)',
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
    'license': 'OPL-1',
    'website': 'https://coa-egy.odoo.com/',
    'price': 29.0,
    'currency': 'USD',
}
