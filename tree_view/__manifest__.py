{
    "name": "Owl tree view",
    "summary": "This is view write by owl js fw",
    "author": "VNS",
    "website": "https://vnsolution.com.vn/",
    "category": "Customizations",
    "version": "1.0.0",
    "depends": ["base", "web", "mail", "product"],
    "data": [
        "views/product_views.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "/tree_view/static/src/components/tree_view_item/TreeViewItem.xml",
            "/tree_view/static/src/components/tree_view_item/TreeViewTable.xml",
            "/tree_view/static/src/xml/owl_tree_view_renderer.xml",
        ],
        "web.assets_backend": [
            "/tree_view/static/src/owl_tree_view/owl_tree_view_view.scss",
            "/tree_view/static/src/owl_tree_view/owl_tree_view_view.js",
            "/tree_view/static/src/owl_tree_view/owl_tree_view_model.js",
            "/tree_view/static/src/owl_tree_view/owl_tree_view_renderer.js",

            "/tree_view/static/src/components/tree_view_item/tree_view_item.scss",
            "/tree_view/static/src/components/tree_view_item/TreeViewItem.js",

            "/tree_view/static/src/components/tree_view_item/tree_view_table.scss",
            "/tree_view/static/src/components/tree_view_item/TreeViewTable.js",
        ],
    },
}
