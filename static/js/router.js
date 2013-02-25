define(
  "router",
  ["jquery",
   "backbone",
   "models",
   "views",
   "user"],
  function($, backbone, Models, Views, User) {
    return Backbone.Router.extend({

        initialize: function ()
        {
          this.navigation = new Views.Navigation(this);
          this.startup = $.Deferred();
          this.user = new User();
          var _this = this;
          this.user.authenticate().done(function(user){
            _this.user = user;
            if ( _this.user.authenticated === true )
            {
              _this.navigation.render();
              _this.startup.resolve();
            } else {
              document.location = '/login';
            }
          });
        },

        render_dashboard: function ()
        {
            //Apiary.render_template("pages/dashboard", {user: User}, render_page);
            //Apiary.set_active_navbar_item("");
        },

        render_settings_distributions: function ()
        {
          if (this.distributions === undefined)
          {
            this.distributions = new Views.Distributions();
          } else {
            this.distributions.render();
          }
        },

        render_systems: function ()
        {
          if (this.systems === undefined)
          {
            this.systems = new Views.Systems();
          }
          this.systems.render();
        },

        render_system: function (id)
        {
            var self = this;
            this.model = new Models.System({id: id});
            this.model.fetch({success: function(){
                self.view = new Views.System(self.model);
                self.view.render();
            }});
        },

        routes: {"": "render_dashboard",
            "settings/distributions": "render_settings_distributions",
            "settings/distribution/:name": "render_settings_distribution",
            "systems": "render_systems",
            "system/:id": "render_system"}
    });
});
