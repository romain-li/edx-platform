define(['hello_require/assets/js/utils'], function(Utils){
    function HelloRequire(runtime, element) {
        Utils.show_message("Hello RequireJS");
    }

    return HelloRequire;
});