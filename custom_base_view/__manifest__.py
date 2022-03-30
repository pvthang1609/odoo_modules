{
    'name': 'Custom base view',
    'application': True,
    'author': "VN Solutions",
    'description': """
    Mục đích của module này là override các base view, thêm icon vào phần controll panel
    """,
    'depends': [
        'base',
        'web',
    ],
    'data': [],
    'assets': {
            'web.assets_backend': [
                'custom_base_view/static/src/css/style.css',
                'custom_base_view/static/src/js/format_number.js',
                'custom_base_view/static/src/js/list_renderer_inherit.js',
            ],
            'web.assets_qweb': [
                'custom_base_view/static/src/xml/base.xml',
            ],
    }
}