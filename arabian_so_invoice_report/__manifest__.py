# -*- coding: utf-8 -*-
{
    'name': 'arabian_so_invoice_report',
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': "\nLong description of module's purpose\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.0.1',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale', 'account', 'l10n_gcc_invoice'],
    'data': ['report/invoice_template.xml', 'report/sale_order_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
