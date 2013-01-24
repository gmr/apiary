// Apiary JavaScript

// @codekit-prepend "src/distributions.js";

var routes = {
    "/settings/distributions": [{path: "",
                                 name: "Distributions",
                                 callback: DistributionsTableView.initialize}]
};

var Router = Backbone.Router.extend({

    initialize: function() {
        var self = this;
        _.each(routes[document.location.pathname], function(route) {
            self.route(route.path, route.name, route.callback);
        });
    }
});

function bind_popovers()
{
    $("[rel='popover']").popover();
}

function bind_tooltips()
{
    $("[rel='tooltip']").tooltip();
}

$(function() {
    new Router();
    Backbone.history.start();
    bind_tooltips();
    bind_popovers();
});
