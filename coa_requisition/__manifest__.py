# -*- coding: utf-8 -*-
{
    'name': "coa_requisition",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Community of accountants (COA-Egypt)",
    'website': "https://www.coa-egy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','uom','stock','purchase', 'purchase_requisition'],

    # always loaded
    'data': [
        'security/construction_requisition_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/construction_requisition.xml',
        'views/purchase_agreements.xml',
        'views/purchase_order.xml',
        'views/stock_picking.xml',
        'wizard/transfer_requisition_order.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

