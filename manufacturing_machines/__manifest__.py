# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing Machines & Maintenance',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'إدارة الآلات والصيانة وتتبع التكاليف في التصنيع',
    'description': """
        نظام متكامل لإدارة:
        - الآلات ومراكز الإنتاج
        - الصيانة الوقائية والتصحيحية
        - تتبع تكاليف العمال والمواد
        - التكاليف الإضافية (Overhead)
        - الربط بالحسابات تلقائياً
    """,
    'author': 'COA (Community of Accountants)',
    'depends': ['base', 'mail', 'account', 'stock', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'views/machine_views.xml',
        'views/maintenance_views.xml',
        'views/production_order_views.xml',
        'views/cost_views.xml',
        'views/mrp_production_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
