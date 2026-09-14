{
    'name': 'Duplicate Company Data PRO',
    'version': '19.0.1.0.0',
    'category': 'Administration',
    'summary': 'Seamlessly duplicate Chart of Accounts, Taxes, Journals, and Warehouses for Multi-Company Setup',
    'description': """
        This module allows you to safely duplicate essential accounting and inventory configurations 
        from one company to another in a multi-company environment.
        Fully compatible with Odoo 19 new shared accounts architecture.
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'website': 'https://www.coa-egy.com',
    'images': ['static/description/banner.png'],
    'depends': ['base', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_views.xml',
    ],
    # --- ده الجزء الخاص بالفلوس والبيع ---
    'price': 49.99, # حط السعر اللي إنت شايفة مناسب (أنصحك تبدأ بـ 45 مثلاً)
    'currency': 'USD', # أو EUR
    'license': 'OPL-1', # مهم جداً!! ده الترخيص اللي بيمنع الناس تنشر الكود بتاعك مجاناً
    'images': ['static/description/banner.png'], # صورة البانر اللي هتظهر في المتجر
    'installable': True,
    'application': False,
    'auto_install': False,
}