# -*- coding: utf-8 -*-
{
    'name': 'Alramlaa Technical Office',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Technical Office review workflow between Sale Orders and Manufacturing',
    'description': """
        Adds a Technical Office approval layer between Sale Orders and Manufacturing.

        Features
        --------
        * "Request Technical Review" button on Sale Order
        * One technical.review record per SO with per-product review lines
        * BOM auto-detection per product; create estimated BOM if none exists
        * Approve / Reject workflow with mandatory rejection reason
        * Blocks SO confirmation until the review is approved
        * Integrates with alramlaa_product_dimensions (dimension fields on products & BOM)
        * Full mail.thread + mail.activity.mixin on the review record
        * Sequence-generated reference (TR/YYYY/MM/0001)
        * Security groups: Technical Office User / Manager
    """,
    'author': 'COA (Community of Accountants)',
    'depends': [
        'sale_management',
        'mrp',
        'mail',
        'alramlaa_product_dimensions',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'wizard/reject_wizard_views.xml',
        'views/technical_review_views.xml',
        'views/sale_order_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
