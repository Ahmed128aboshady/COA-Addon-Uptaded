# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Inventory/Stock Aging Report',
    'version': '19.0.1.0.0',
    'summary': 'Analyze the age of stock by grouping quantities into time periods.',
    'description': """Aging Analysis: Group stock age by warehouse or specific storage locations.
Filters: Filter results by products, product categories, or dates.
Aging Buckets: Configurable aging periods (0-30 days, 31-60 days, etc.).
Exports: Supports detailed PDF/Excel export.""",
    'category': 'Inventory/Inventory',
    'author': 'Community of Accountants (COA)',
    'website': 'https://coa-egy.odoo.com/',
    'license': 'OPL-1',
    'depends': [
        'stock',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_aging_wizard_view.xml',
        'report/stock_aging_report_action.xml',
        'report/stock_aging_report_template.xml',
        'data/stock_aging_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 79.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
