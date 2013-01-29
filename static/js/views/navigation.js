define([
    "jquery",
    "backbone",
    "apiary_tools"
], function($, backbone, ApiaryTools) {

    var NavigationView = Backbone.View.extend({

        on_rendered: function(content) {
            $("#navbar").html(content);
        },

        render:function() {
            ApiaryTools.render_template("snippets/navigation", {user: document.router.user}, this.on_rendered);
        },

        tagName: "div"

    });

    return NavigationView;

});
