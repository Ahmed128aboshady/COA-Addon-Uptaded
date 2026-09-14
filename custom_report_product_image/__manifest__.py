{
    'website': 'https://www.coa-egy.com',
    'name': 'Custom Reports — Product Image & Reference Code',
    'version': '19.0.1.0.0',
    'category': 'Technical',
    'summary': 'Adds product image to Delivery prints and splits product name / reference code into separate columns across all module reports',
    'description': """
        Customises printed reports for:
        - Inventory / Delivery Orders  : adds product image column + separate Reference column
        - Sales Orders / Quotations    : adds separate Reference column
        - Purchase Orders              : adds separate Reference column
        - Invoices & Bills             : adds separate Reference column

        The "Reference" column shows the product's Internal Reference (default_code).
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['stock', 'sale_management', 'purchase', 'account'],
    'data': [
        'report/report_delivery_custom.xml',
        'report/report_sale_custom.xml',
        'report/report_purchase_custom.xml',
        'report/report_invoice_custom.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
