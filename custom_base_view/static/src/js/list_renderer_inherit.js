odoo.define("list_renderer_inherit.main", function (require) {
    "use strict";
    var ListRenderer = require("web.ListRenderer");
    /**
    * We want to remove _renderEmptyRow().
    *
    * @override
    * @private
    */
    ListRenderer.include({
        _renderBody: function () {
            var self = this;
            var $rows = this._renderRows();
            return $('<tbody>').append($rows);
        },
    });
})
