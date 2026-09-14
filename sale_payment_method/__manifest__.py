{
    'website': 'https://www.coa-egy.com',
    'author': 'Community of accountants (COA-Egypt)',
    'name': 'Sale Payment Method',
    'version': '19.0.1.0.0',
    'summary': 'Add payment method tags on sales orders and invoices with reporting',
    'category': 'Accounting/Reporting',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_method_data.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/report_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
