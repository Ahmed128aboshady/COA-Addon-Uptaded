# -*- coding: utf-8 -*-
{
    'name': 'Customer Portal: Order Request',
    'version': '18.0.1.0.0',
    'summary': 'Empower customers to search products, select addresses, and request new sales quotations directly from their portal.',
    'description': """
Customer Portal Order Request for Odoo
======================================
Boost your sales efficiency and customer satisfaction by offering a seamless self-service ordering interface inside the Odoo Customer Portal.

Key Features:
-------------
* **Instant Product Search**: Customers can search for items by name or barcode with live autocomplete suggestions.
* **Rich Product Details**: Displays high-quality product images, internal reference codes, pricing, and units of measure (UoM).
* **Multi-Address Support**: Customers can select separate shipping and billing addresses associated with their account.
* **Custom Instructions**: Provides a dedicated field for delivery instructions or special order notes.
* **Auto-Quotation Creation**: Instantly generates draft Sale Orders (quotations) in the Odoo backend, sets them to 'Quotation Sent', and sends notifications.
* **Confirmation Receipt**: Displays a professional confirmation screen with the generated quotation number and details.
* **Mobile Responsive**: Fully optimized for mobile, tablet, and desktop viewports.

This module is the perfect solution for B2B portal orders, wholesale customer portals, and quick reordering systems.
    """,
    'author': 'Community of Accountants',
    'website': 'https://www.communityofaccountants.com',
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
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.png',
    ],
}
