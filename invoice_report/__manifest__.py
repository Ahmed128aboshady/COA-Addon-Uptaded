# -*- encoding: UTF-8 -*-
{
    'name': 'invoice_report',
    'version': '19.0.1.0.0',
     "author": 'Community of accountants (COA-Egypt)',
     "company": 'arabian open source',
     "website": "",
     "email": "",
    'category': 'Accounting',
    'sequence': 1,
    'summary': 'invoice_report',
    'description': """
    this module use for print journal Entries in PDF report"
    """,
    'depends': ['account'],
    'data': [
        'report/report.xml'
    ],
    "price": 0.00,
    "currency": 'EUR',
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    "application": True,
    'images': ['static/description/journal.png'],
}
