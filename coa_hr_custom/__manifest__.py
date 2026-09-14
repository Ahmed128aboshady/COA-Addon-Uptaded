{
    'name': 'Al-Ramlaa HR Customization',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Custom HR fields for Al-Ramlaa Project (Family & Insurance)',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}