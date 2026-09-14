{
    'website': 'https://www.coa-egy.com',
    'name': 'BOM Formula Calculator',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'إضافة حاسبة معادلات ديناميكية على BOM',
    'description': """
        يضيف تاب "حاسبة التصنيع" على BOM يمكّنك من:
        - تعريف متغيرات (طول، عرض، سماكة، عدد، ثوابت)
        - كتابة معادلات Python يدوياً لكل component
        - حساب الكميات تلقائياً وتحديث BOM Lines
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/bom_formula_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
