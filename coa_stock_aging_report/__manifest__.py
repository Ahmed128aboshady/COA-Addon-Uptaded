# -*- coding: utf-8 -*-
{
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Inventory/Stock Aging Report',
    'version': '19.0.1.0.0',
    'summary': 'Stock Aging Report By Warehouse and By Location',
    'description': """
        Stock Aging Report
        ==================
        The stock aging analysis report helps you analyze the age of your stock
        by organizing the value and quantity into configurable time periods.

        Features:
        - Stock Aging Report by Warehouse
        - Stock Aging Report by Location
        - Filter by Products or Product Categories
        - Configurable aging periods (e.g. 0-30, 31-60, 61-90, 91-120, 120+ days)
        - PDF Export
        - FIFO-based age calculation
    """,
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
