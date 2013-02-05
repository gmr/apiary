var User = {
    authenticated: false,
    initialize: function() {
        $.ajax({
            url: '/profile',
            type: 'GET',
            success: function(data){
              User.authenticated = true;
              User.profile = data;
              document.router.navigation_view.render();
            },
            error: function() {
              document.location = '/login';
            }
        });
    },
    profile: {}
};
