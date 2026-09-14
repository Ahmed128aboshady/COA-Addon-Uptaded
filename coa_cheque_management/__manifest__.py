# -*- coding: utf-8 -*-
{
    'name': "COA Cheque Management | إدارة الشيكات والأوراق المالية",
    'summary': "نظام إدارة دورة حياة الشيكات الواردة والصادرة والربط المحاسبي الكامل على أودو 19 - COA Egypt",
    'description': """
COA Cheque Management System for Odoo 19
========================================
نظام متكامل لإدارة الشيكات والأوراق التجارية (وارد وصادر):
- إدارة شيكات المبيعات والعملاء (Incoming Cheques).
- إدارة شيكات المشتريات ومقاولي الباطن (Outgoing Cheques).
- الربط التلقائي بقيود اليومية وأوراق القبض والدفع.
- تتبع ومراقبة الحالات: مسودة، تأكيد، إيداع/تسوية، إلغاء وارتداد.
- ربط المشاريع ومراكز التكلفة والمقاولات.
    """,
    'author': "Community of accountants (COA-Egypt)",
    'website': "https://www.coa-egy.com",
    'category': 'Accounting/Accounting',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
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