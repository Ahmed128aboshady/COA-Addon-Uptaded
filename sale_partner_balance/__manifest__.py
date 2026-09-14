{
    'name': 'Sale Partner Balance',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Display partner previous and current balance on Sale Order and Invoice reports',
    'description': """
        This module adds a balance section to Sale Order and Invoice reports showing:
        - Previous Balance (الرصيد السابق)
        - Current Document Amount (الفاتورة الحالية)
        - Current Balance (الرصيد الحالي)
    """,
    'author': 'COA (Community of Accountants)',
    'depends': ['sale', 'account'],
    'data': [
        'report/sale_report_templates.xml',
        'report/invoice_report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
