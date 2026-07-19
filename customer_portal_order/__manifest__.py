# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Customer Portal: Order Request',
    'version': '18.0.1.0.0',
    'summary': 'Empower customers to search products, select addresses, and request quotations.',
    'description': """Portal Search: Search products by name, barcode, or reference code with autocomplete.
Rich UI: Displays product images, detailed specifications, and customer-specific pricing.
Addresses: Allows customers to select delivery address and shipping methods.
Quotation Request: Instantly generates draft sale quotations in the backend.""",
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'category': 'Sales',
    'depends': [
        'sale_management',
        'portal',
        'website',
    ],
    'data': [
        'views/portal_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'customer_portal_order/static/src/js/portal_order.js',
        ],
    },
    'price': 59.0,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'images': [
        'static/description/banner.png',
    ],
}
