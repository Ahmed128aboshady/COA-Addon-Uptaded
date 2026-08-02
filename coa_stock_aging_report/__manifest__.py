# -*- coding: utf-8 -*-
{
    'name': 'COA Stock Aging Report',
    'summary': 'Analyze the age of stock by grouping quantities into time periods.',
    'description': 'Aging Analysis: Group stock age by warehouse or specific storage locations.\nFilters: Filter results by products, product categories, or dates.\nAging Buckets: Configurable aging periods (0-30 days, 31-60 days, etc.).\nExports: Supports detailed PDF/Excel export.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Inventory',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['stock', 'mail'],
    'data': ['security/ir.model.access.csv', 'wizard/stock_aging_wizard_view.xml', 'report/stock_aging_report_action.xml', 'report/stock_aging_report_template.xml', 'data/stock_aging_menu.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
