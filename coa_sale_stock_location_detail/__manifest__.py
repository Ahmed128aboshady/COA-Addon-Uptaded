# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Stock Location Detail',
    'summary': 'Show reserved sub-locations per SO line (from stock.move.line) in SO, invoice & print',
    'description': 'COA Sale Stock Location Detail developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 18.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Sales',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 29.0,
    'currency': 'EUR',
    'depends': ['sale_stock', 'account'],
    'data': ['security/ir.model.access.csv', 'views/sale_order_views.xml', 'report/sale_order_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
