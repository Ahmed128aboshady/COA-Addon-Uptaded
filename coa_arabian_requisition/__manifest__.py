# -*- coding: utf-8 -*-
{
    'name': 'COA Arabian Requisition',
    'summary': 'Professional Arabian Requisition solution for Odoo Project. Streamlines business operations, automates workflow validations, an...',
    'description': 'COA Arabian Requisition developed by COA Egypt (https://www.coa-egy.com). Silicon Valley grade solution for Odoo 17.0.0.1.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Project',
    'version': '1.0.0',
    'license': 'OPL-1',
    'price': 59.0,
    'currency': 'EUR',
    'depends': ['base', 'hr', 'uom', 'stock', 'purchase', 'purchase_requisition'],
    'data': ['security/construction_requisition_groups.xml', 'security/ir.model.access.csv', 'views/views.xml', 'views/templates.xml', 'views/construction_requisition.xml', 'views/purchase_agreements.xml', 'views/purchase_order.xml', 'views/stock_picking.xml', 'wizard/transfer_requisition_order.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
