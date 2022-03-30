odoo.define('ext_sale.rate', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');

    var RateWidget = basic_fields.FieldInteger.extend({
        _renderReadonly: function () {
            this._super();
            const star = '<span class="text-warning fa fa-star"></span>'
            const starO = '<span class="fa fa-star"></span>'
            const starHalfO = '<span class="text-warning fa fa-star-half-o"></span>'
            let newHTML = ""
            for(let i = 0; i < Math.ceil(this.value); i++) {
                if(!Number.isInteger(this.value) && i === Math.ceil(this.value)) {
                    newHTML = newHTML + starHalfO
                } else {
                    newHTML = newHTML + star
                }
            }
            for(let i = 0; i < 5 - Math.floor(this.value); i++) {
                newHTML = newHTML + starO
            }
            this.$el.html(newHTML);
        },
    });

    registry.add('rate_readonly', RateWidget); // add our "bold" widget to the widget registry
});