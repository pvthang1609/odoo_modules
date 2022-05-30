{
    'name': 'Custom Title',
    'application': True,
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'views/webclient_templates.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/custom_title/static/src/js/**/*',
            '/custom_title/static/src/css/**/*',
        ],
        'web.assets_qweb': [
            '/custom_title/static/src/xml/**/*',
        ],
    }
}
