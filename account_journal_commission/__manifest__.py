# -*- coding: utf-8 -*-
{
    'description': """Payment Integration: Automatically calculates and deducts commission when posting payments.
Journal Commission: Supports separate rules for sales and purchase payment journals.
Automatic Entries: Automatically handles journal entry generation for commission deductions.
Unified Workflow: Fully integrated with Odoo accounting workflows.""",
    'support': 'https://api.whatsapp.com/send?phone=201013907174',
    'name': 'Journal Payment Commission',
    'version': '18.0.1.0.0',
    'summary': 'Automate commission deductions on payments for configured sales and purchase journals.',
    'author': 'Community of Accountants (COA)',
    'category': 'Accounting',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/account_payment_views.xml',
        'views/account_payment_register_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'website': 'https://coa-egy.odoo.com/',
    'price': 49.0,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
    ],
}
