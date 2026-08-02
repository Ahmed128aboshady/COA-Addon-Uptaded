# -*- coding: utf-8 -*-
{
    'name': 'COA Sr Stock Aging Report',
    'summary': 'Stock Aging Report By Warehouse and By Location',
    'description': '\n        Stock Aging Report\n        ==================\n        The stock aging analysis report helps you analyze the age of your stock\n        by organizing the value and quantity into configurable time periods.\n\n        Features:\n        - Stock Aging Report by Warehouse\n        - Stock Aging Report by Location\n        - Filter by Products or Product Categories\n        - Configurable aging periods (e.g. 0-30, 31-60, 61-90, 91-120, 120+ days)\n        - PDF Export\n        - FIFO-based age calculation\n    ',
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
