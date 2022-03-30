odoo.define('helloworld.main', function (require) {
    "use strict";
    const alertNotifi = (message) => {
        alert(message)
    }
//    alertNotifi("Thông báo")
    return alertNotifi;
})