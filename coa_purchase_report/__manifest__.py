{
    'name': 'Arfad Custom Purchase Report',
    'version': '19.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Custom PDF layout for Purchase Orders',
    'description': """
        Replaces the default Odoo Purchase Order PDF with a custom 
        layout matching Arfad company design.
    """,
    'author': 'COA (Community of Accountants)',
    'depends': ['purchase'],
    'data': [
        'views/report_purchaseorder_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}