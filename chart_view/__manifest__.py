{
    'name': 'Chart',
    'application': True,
    'author': "VN Solutions",
    'description': """
    Demo kết hợp chart-js
    """,
    'depends': [
        'base',
        'web',
        'sale_management',
        'account',
        'stock',
        'purchase'
    ],
    'data': [
        'views/chart.xml',
        'views/menu_views.xml'
    ],
    'assets': {
            'web.assets_backend': [
                'chart/static/src/css/style.css',

                'chart/static/src/js/lib/chart_js/chart.js',
                'chart/static/src/js/chart_view.js',
            ]
    }
}
