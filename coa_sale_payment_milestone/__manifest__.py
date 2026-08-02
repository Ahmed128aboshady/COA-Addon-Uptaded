# -*- coding: utf-8 -*-
{
    'name': 'COA Sale Payment Milestone',
    'summary': 'شروط سداد بالمراحل مع ربط مباشر بالمدفوعات المحاسبية',
    'description': 'COA Sale Payment Milestone developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Accounting',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 35.0,
    'currency': 'EUR',
    'depends': ['sale_management', 'account'],
    'data': ['security/ir.model.access.csv', 'data/mail_template_data.xml', 'views/sale_payment_milestone_views.xml', 'views/sale_order_views.xml', 'wizard/milestone_reconcile_wizard_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
