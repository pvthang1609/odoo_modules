{
    'name': 'Extension Sale for DIMO',
    'application': True,
    'depends': [
        'base',
        'web',
        'sale',
        'purchase',
        'hr',
        'sale_management',
        'product',
        'report_xlsx'
    ],
    'data': [
        'security/sale_security.xml',
        'security/access_rules.xml',
        'security/ir.model.access.csv',
        'views/ir_sequence_data.xml',
        'views/purchase_price_list_product_view.xml',
        'views/purchase_price_line_views.xml',
        'views/product_template_views.xml',
        'views/purchase_views.xml',
        'views/reason_views.xml',
        'views/currency_views.xml',
        'wizard/approve_wizard.xml',
        'wizard/reason_wizard.xml',
        'wizard/askinfo_product_actions_wizard.xml',
        'views/sale_order_line_views.xml',
        'views/config_parameter_views.xml',
        'views/res_partner_views.xml',
        'views/askinfo_product_views.xml',
        'views/askinfo_product_line_views.xml',
        'report/report.xml',
        'views/sale_order_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'ext_sale/static/src/css/style.css',
                'ext_sale/static/src/js/helloworld.js',
                'ext_sale/static/src/js/rate_readonly.js',
            ],
    }
}
