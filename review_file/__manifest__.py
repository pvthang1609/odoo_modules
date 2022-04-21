{
    'name': 'Review file',
    'application': True,
    'author': "VN Solutions",
    'description': """
    Module review tài liệu pdf, text...
    """,
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'views/review_file.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'review_file\\static\\src\\js\\field_binary_file_uploader.js',
            'review_file\\static\\src\\js\\iframe_controller.js',
            'review_file\\static\\src\\js\\iframe_model.js',
            'review_file\\static\\src\\js\\iframe_renderer.js',
            'review_file\\static\\src\\js\\iframe_view.js',
        ],
        'web.assets_qweb': [
            'review_file\\static\\src\\xml\\field_binary_file_uploader.xml'
        ],
    }
}