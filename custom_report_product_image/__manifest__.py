# -*- coding: utf-8 -*-
{
    'name': 'Custom Reports — Product Image & Reference Code',
    'summary': 'Adds product image to Delivery prints and splits product name / reference code into separate columns across all modul...',
    'description': '\n        Customises printed reports for:\n        - Inventory / Delivery Orders  : adds product image column + separate Reference column\n        - Sales Orders / Quotations    : adds separate Reference column\n        - Purchase Orders              : adds separate Reference column\n        - Invoices & Bills             : adds separate Reference column\n\n        The "Reference" column shows the product\'s Internal Reference (default_code).\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Extra Tools',
    'version': '17.0.19.0.1.0.0',
    'license': 'LGPL-3',
    'price': 19.0,
    'currency': 'EUR',
    'depends': ['stock', 'sale_management', 'purchase', 'account'],
    'data': ['report/report_delivery_custom.xml', 'report/report_sale_custom.xml', 'report/report_purchase_custom.xml', 'report/report_invoice_custom.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
