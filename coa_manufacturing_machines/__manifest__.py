# -*- coding: utf-8 -*-
{
    'name': 'COA Manufacturing Machines',
    'summary': 'إدارة الآلات والصيانة وتتبع التكاليف في التصنيع',
    'description': '\n        نظام متكامل لإدارة:\n        - الآلات ومراكز الإنتاج\n        - الصيانة الوقائية والتصحيحية\n        - تتبع تكاليف العمال والمواد\n        - التكاليف الإضافية (Overhead)\n        - الربط بالحسابات تلقائياً\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Manufacturing',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock', 'mrp'],
    'data': ['security/ir.model.access.csv', 'security/security.xml', 'data/sequence.xml', 'views/machine_views.xml', 'views/maintenance_views.xml', 'views/production_order_views.xml', 'views/cost_views.xml', 'views/mrp_production_views.xml', 'views/menu_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
