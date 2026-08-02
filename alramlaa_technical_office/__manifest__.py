# -*- coding: utf-8 -*-
{
    'name': 'COA Alramlaa Technical Office',
    'summary': 'Technical Office review workflow between Sale Orders and Manufacturing',
    'description': 'COA Alramlaa Technical Office developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
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
