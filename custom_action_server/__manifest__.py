{
    'name': 'Custom action server',
    'application': True,
    'author': "VN Solutions",
    'description': """
    Mục đích của module này là override model ir.action.server để lưu trữ thêm dữ liệu hiển thị (icon) sau đó render dưới client
    """,
    'depends': [
        'base',
        'web',
    ],
    'data': [],
    'assets': {
            'web.assets_backend': [
                'custom_action_server/static/src/js/action_menu.js',
                'custom_action_server/static/src/css/style.css',
            ],
            'web.assets_qweb': [
                'custom_action_server/static/src/xml/base.xml',
            ],
    }
}