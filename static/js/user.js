define([
    "jquery",
    "backbone",
    "apiary_tools"
], function($, Backbone, ApiaryTools) {

    var User = {

        authenticated: false,

        initialize: function() {
            $.ajax({
                url: '/profile',
                type: 'GET',
                success: function(data){
                    User.authenticated = true;
                    User.profile = data;
                    document.router.render_navbar();
                },
                error: function(data) {
                    document.location = '/login';
                }
            });
        },

        profile: {}

    };

    return User;

});
