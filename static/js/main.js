// Apiary Main JavaScript Loader

require.config({
    paths: {
        apiary_tools: "libs/apiary-tools/apiary-tools",
        backbone: "libs/backbone/backbone.min",
        bootstrap: "libs/bootstrap/bootstrap.min",
        dust: "libs/dust/dust.min",
        "dust-helpers": "libs/dust-helpers/dust-helpers.min",
        jquery: "libs/jquery/jquery.min",
        tableview: "src/tableview",
        underscore: "libs/underscore/underscore.min"
    },
    shim: {
        "backbone": {
            deps: ["underscore", "jquery"],
            exports: "Backbone"
        },
        dust: {
            exports: "dust"
        },
        "dust-helpers": {
            deps: ["dust"],
            exports: "dust-helpers"
        },
        "bootstrap": {
            deps: ["jquery"],
            exports: "bootstrap"
        },
        underscore: {
            exports: "_"
        }
    },
    urlArgs: "req=" +  (new Date()).getTime()
});

require ([
    "apiary"
], function(Apiary) {
    return Apiary.initialize();
});
