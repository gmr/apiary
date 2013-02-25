/**
 * Apiary Main Loader
 *
 * @since 2013-02-24
 */
require.config({baseUrl: "/static/js",
                paths: {
                  "backbone": "libs/backbone/backbone.min",
                  "jquery": "libs/jquery/jquery.min",
                  "bootstrap": "libs/bootstrap/bootstrap.min",
                  "transparency": "libs/transparency/transparency.min",
                  "metadata": "libs/jquery.metadata/jquery.metadata",
                  "jquery.tablesorter": "libs/jquery.tablesorter/jquery.tablesorter",
                  "jquery.tablesorter.pager": "libs/jquery.tablesorter/jquery.tablesorter.pager",
                  "jquery.tablesorter.widgets": "libs/jquery.tablesorter/jquery.tablesorter.widgets",
                  "underscore": "libs/underscore/underscore.min"
                },
                shim: {
                  "backbone": {
                    deps: ["underscore", "jquery"],
                    exports: "Backbone"
                  },
                  "bootstrap": {
                    deps: ["jquery"],
                    exports: "bootstrap"
                  },
                  "jquery.tablesorter": {
                    deps: ["jquery"]
                  },
                  "jquery.tablesorter.pager": {
                    deps: ["jquery.tablesorter"]
                  },
                  "jquery.tablesorter.widgets": {
                    deps: ["jquery.tablesorter"]
                  },
                  "transparency": {
                    deps: ["jquery"],
                    exports: "Transparency"
                  },
                  underscore: {
                    exports: "_"
                  }
                },
                urlArgs: "req=" +  (new Date()).getTime()
              });

require (["apiary", "backbone", "transparency", "view_tools"], function(Apiary, Backbone, Transparency, ViewTools) {
  Transparency.matcher = function(element, key) {
    return element.getAttribute('data-bind') === key;
  };

  document.view_tools = new ViewTools();
  document.apiary = new Apiary();
  document.apiary.router.startup.done(function(){
    Backbone.history.start();
  });
});
