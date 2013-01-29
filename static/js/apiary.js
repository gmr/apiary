define([
    "jquery",
    "backbone",
    "bootstrap",
    "dust",
    "apiary_tools",
    "user",
    "views"
], function($, backbone, bootstrap, dust, ApiaryTools, User, Views) {

    var initialize = function() {

        function render_page(content)
        {
            $("#content").html(content);
        }

        var Router = Backbone.Router.extend({

            routes:  {"": "render_dashboard",
                      "settings/distributions": "render_settings_distributions",
                      "settings/distribution/:id": "render_settings_distribution"},

            initialize: function() {
                this.user = User;
                this.user.initialize();
            },

            render_navbar: function() {
                if (!this.navigation_view) {
                    this.navigation_view = new Views.NavigationView();
                }
                this.navigation_view.render();
            },

            render_dashboard: function() {
                ApiaryTools.render_template("pages/dashboard", {user: User}, render_page);
                ApiaryTools.set_active_navbar_item("");
            },

            render_settings_distributions: function () {
                if (!this.distributions_view) {
                    this.distributions_view = Views.DistributionsView.initialize();
                }
            },

            user: null

        });

        ApiaryTools.dispatcher.on("dust:compilation_complete", function(message) {
            document.router = new Router();
            Backbone.history.start();

        });
    };



    return {
        initialize: initialize
    };


});
