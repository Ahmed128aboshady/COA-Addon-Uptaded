{
    'website': 'https://www.coa-egy.com',
    'author': 'Community of accountants (COA-Egypt)',
    'name': 'Al-Ramlaa Custom HR Updates',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Customizations for HR Units, Departments, and Kafala Status',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_custom_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}