# -*- coding: utf-8 -*-
{
    'name': "arabian_construction_managment",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "COA (Community of Accountants)",
    'website': "https://www.coa-egy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'uom', 'account', 'purchase', 'utm', 'project',
                'arabian_cheque_management', 'arabian_requisition','stock',
                'arabian_letters_of_guarantee','documents','arabian_expense_payment','arabian_res_partner','hr_timesheet'],

    # always loaded
    'data': [
        'security/construction_groups.xml',
        'security/ir.model.access.csv',
        'data/data_contracting_project_classification.xml',
        'data/data_construction_project_type.xml',
        'data/data_business_items_types.xml',
        'data/data_detailed_business_items.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/construction_project.xml',
        'views/construction_project_type.xml',
        'views/construction_business_items.xml',
        'views/business_items_types.xml',
        'views/detailed_business_items.xml',
        'views/contracting_project_classification.xml',
        'views/detailed_bill_of_quantities.xml',
        'views/boq_cost_estimation.xml',
        'views/construction_pricing.xml',
        'views/project_project.xml',
        'views/cheque_management.xml',
        'views/project_task.xml',
        'views/construction_subcontractor.xml',
        'views/interim_invoice.xml',
        'views/construction_requisition.xml',
        'views/advance_payment_guarantee.xml',
        'views/bid_bond.xml',
        'views/maintenance_bond.xml',
        'views/performance_bond.xml',
        'views/expense_payment.xml',
        'views/account_move.xml',
        'views/account_payment.xml',
        'views/project_task.xml',
        'views/time_sheet_report.xml',
        'views/purchase_order.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'views/purchase_requisition.xml',
        'views/purchase_report.xml',
        'wizard/create_business_items.xml',
        'wizard/construction_project_payment.xml',
        'wizard/subcontractor_attribution_boq.xml',
        'wizard/select_detailed_boq_type.xml',


        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
