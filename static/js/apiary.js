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

$(function() {
    new Router();
    Backbone.history.start();
});
