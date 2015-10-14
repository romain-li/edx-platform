define(['xblock-hello-require/public/js/utils'], function(Utils){
    function HelloRequire(runtime, element) {
        Utils.show_message("Hello RequireJS");
    }

    return HelloRequire;
});