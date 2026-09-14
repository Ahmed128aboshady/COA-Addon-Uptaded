{
    'name': 'MFG Component Correction',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'تصحيح كميات المكونات بعد إتمام أوامر التصنيع',
    'description': """
        يتيح هذا الموديول إمكانية تصحيح كميات المكونات المستهلكة
        بعد إغلاق أمر التصنيع، مع إرجاع الفارق للمخزن وتصحيح التكلفة تلقائياً.
    """,
    'author': 'COA (Community of Accountants)',
    'depends': ['mrp', 'stock', 'stock_account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/mrp_component_correction_wizard_view.xml',
        'views/mrp_production_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
