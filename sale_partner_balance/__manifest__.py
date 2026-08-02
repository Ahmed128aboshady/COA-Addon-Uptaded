# -*- coding: utf-8 -*-
{
    'name': 'Sale Partner Balance',
    'summary': 'Display partner previous and current balance on Sale Order and Invoice reports',
    'description': '\n        This module adds a balance section to Sale Order and Invoice reports showing:\n        - Previous Balance (الرصيد السابق)\n        - Current Document Amount (الفاتورة الحالية)\n        - Current Balance (الرصيد الحالي)\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.19.0.2.0.0',
    'license': 'LGPL-3',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale', 'account'],
    'data': ['report/sale_report_templates.xml', 'report/invoice_report_templates.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
