# -*- coding: utf-8 -*-
{
    'name': 'COA Alramlaa Technical Office',
    'summary': 'Technical Office review workflow between Sale Orders and Manufacturing',
    'description': '\n        Adds a Technical Office approval layer between Sale Orders and Manufacturing.\n\n        Features\n        --------\n        * "Request Technical Review" button on Sale Order\n        * One technical.review record per SO with per-product review lines\n        * BOM auto-detection per product; create estimated BOM if none exists\n        * Approve / Reject workflow with mandatory rejection reason\n        * Blocks SO confirmation until the review is approved\n        * Integrates with alramlaa_product_dimensions (dimension fields on products & BOM)\n        * Full mail.thread + mail.activity.mixin on the review record\n        * Sequence-generated reference (TR/YYYY/MM/0001)\n        * Security groups: Technical Office User / Manager\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Project',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 79.0,
    'currency': 'EUR',
    'depends': ['sale_management', 'mrp', 'mail', 'alramlaa_product_dimensions'],
    'data': ['security/security.xml', 'security/ir.model.access.csv', 'data/ir_sequence.xml', 'wizard/reject_wizard_views.xml', 'views/technical_review_views.xml', 'views/sale_order_views.xml', 'views/menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
