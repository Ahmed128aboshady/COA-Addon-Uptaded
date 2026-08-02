# -*- coding: utf-8 -*-
{
    'name': 'arabian_requisition',
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': "\nLong description of module's purpose\n    ",
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Project',
    'version': '17.0.0.1',
    'license': 'LGPL-3',
    'price': 59.0,
    'currency': 'EUR',
    'depends': ['base', 'hr', 'uom', 'stock', 'purchase', 'purchase_requisition'],
    'data': ['security/construction_requisition_groups.xml', 'security/ir.model.access.csv', 'views/views.xml', 'views/templates.xml', 'views/construction_requisition.xml', 'views/purchase_agreements.xml', 'views/purchase_order.xml', 'views/stock_picking.xml', 'wizard/transfer_requisition_order.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
