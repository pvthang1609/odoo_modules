{
    "name": "VNSolution Notify",
    "summary": """
        Module gửi thông báo""",
    "license": "AGPL-3",
    "author": "thangpv",
    "depends": ["web", "bus", "base", 'mail'],
    "data": [
        'security/ir.model.access.csv',
        'security/vns_access_rule.xml',

        'views/vns_notification_views.xml',

        'views/vns_menu_item.xml',
    ],
    "assets": {
        "web.assets_qweb": [
            'vns_notify/static/src/components/**/*',
            'vns_notify/static/src/xml/**/*',
        ],
        "web.assets_backend": [
            'vns_notify/static/src/components/**/*',
            'vns_notify/static/src/js/**/*'
        ],
    },
}