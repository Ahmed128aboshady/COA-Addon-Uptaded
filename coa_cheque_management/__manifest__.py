# -*- coding: utf-8 -*-
{
    'name': "COA Cheque Management | Cheque Lifecycle & Accounting",
    'summary': "Complete lifecycle management for incoming customer PDCs and outgoing vendor cheques with automated accounting entries",
    'description': """
COA Cheque Management System for Odoo 19 / 18 / 17
==================================================
Comprehensive financial cheque lifecycle and treasury management system:
- Incoming Cheques Management (Customer Post-Dated Cheques / PDCs).
- Outgoing Cheques Management (Vendor Payments, Subcontractors, Expenses).
- Automated double-entry accounting (Notes Receivable, Notes Payable, Cheques Under Collection, Bank).
- Full status pipeline: Draft, Confirmed, Under Collection, Cleared, and Bounced.
- Automated reversal logic for NSF and returned cheques.
- Analytic distribution and project cost center allocation.
- Fully auditable chatter trail with time-stamped status transitions.
    """,
    'author': "Community of accountants (COA-Egypt)",
    'website': "https://www.coa-egy.com",
    'category': 'Accounting/Accounting',
    'version': '19.0.1.0.0',
    'price': 49.00,
    'currency': 'USD',
    'license': 'OPL-1',
    'depends': ['base', 'account', 'utm'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/cheque_presentation.xml',
        'wizard/check_accounts_cheque.xml',
        'views/incoming_cheque.xml',
        'views/outgoing_cheque.xml',
        'views/res_config_settings.xml',
        'views/account_move.xml',
        'views/menus.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/01_incoming_cheques_list.png',
        'static/description/02_incoming_cheque_form.png',
        'static/description/03_outgoing_cheques_list.png',
        'static/description/04_outgoing_cheque_form.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
