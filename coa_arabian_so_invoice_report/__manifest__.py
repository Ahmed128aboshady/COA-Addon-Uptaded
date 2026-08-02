# -*- coding: utf-8 -*-
{
    'name': 'COA Arabian So Invoice Report',
    'summary': 'Professional Arabian So Invoice Report solution for Odoo Accounting. Streamlines business operations, automates workflow valida...',
    'description': 'COA Arabian So Invoice Report developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.0.1.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.0.1',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale', 'account', 'l10n_gcc_invoice'],
    'data': ['report/invoice_template.xml', 'report/sale_order_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
