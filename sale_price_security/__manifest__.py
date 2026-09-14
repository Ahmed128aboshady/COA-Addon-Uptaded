{
    'website': 'https://www.coa-egy.com',
    'name': 'Sale Price Edit Permission',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Add a checkbox permission to control who can edit sale order prices',
    'description': """
Adds a new group "Can Edit Sale Prices" that appears as a checkbox
in the user access rights page under the Sales section.

When a user does NOT have this permission, the Unit Price field
in sale order lines becomes read-only for them.

By default the group is granted to:
- Administrators
- Sales / Administrator (Sales Manager)
    """,
    'author': 'Community of accountants (COA-Egypt)',
    'depends': ['sale_management'],
    'data': [
        'security/groups.xml',
        'views/sale_order_views.xml',
    ],
    'auto_install': False,
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
