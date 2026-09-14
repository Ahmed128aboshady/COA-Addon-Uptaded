{
    'name': 'Product Color Picker',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Products',
    'summary': 'Color-code products in kanban and list views',
    'depends': ['product'],
    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'product_color_picker/static/src/views/product_color_list/product_color_list_renderer.js',
            'product_color_picker/static/src/views/product_color_list/product_color_list_view.js',
            'product_color_picker/static/src/scss/product_color_list.scss',
        ],
    },
    'pre_init_hook': 'pre_init_hook',
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
