{
    'name': 'Handicrafts management',
    'application': True,
    'author': "VN Solutions",
    'icon': '/handicrafts_management/static/description/icon.png',
    'description': """
    Phần mềm quản lý sản xuất mây tre đan
    """,
    'depends': [
        'base',
        'web',
        'sale_management',
        'stock',
        'purchase',
        'mrp'
    ],
    'data': [
        'views/hm_sale_order_views.xml',
    ],
}
