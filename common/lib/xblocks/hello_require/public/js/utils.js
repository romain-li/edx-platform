(function(define) {
    'use strict';

    define([], function () {
        return {
            show_message: function (message) {
                alert(message);
            }
        }
    });
}).call(this, define || RequireJS.define);