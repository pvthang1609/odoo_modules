{
    'name': 'Custom column width',
    'application': True,
    'author': "VN Solutions",
    'description': """
    Module này cho phép giữ độ rộng mặc định cho 1 table trong list view (Hiện tại oddo đang tính toán để đưa
     ra độ rộng của các cột 1 cách tự động với màn hình) và ghi nhớ độ rộng của cột.
    """,
    'depends': [
        'base',
        'web',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'custom_column_width/static/src/js/list_editable_renderer.js',
            'custom_column_width/static/src/css/style.css'
        ],
        'web.assets_qweb': [],
    }
}
