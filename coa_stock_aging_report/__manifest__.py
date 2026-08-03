# -*- coding: utf-8 -*-
{
    'name': 'COA Stock Aging Report',
    'summary': 'Analyze the age of stock by grouping quantities into time periods.',
    'description': 'COA Stock Aging Report developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Inventory',
    'version': '1.0.0',
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
