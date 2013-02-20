
var Router = Backbone.Router.extend({

    initialize: function()
    {
      console.log('Initialize');
        this.user.initialize();
        if (!this.navigation_view)
        {
            this.navigation_view = new Views.NavigationView();
        }
    },

    render_dashboard: function()
    {
        //Apiary.render_template("pages/dashboard", {user: User}, render_page);
        //Apiary.set_active_navbar_item("");
    },

    render_settings_distributions: function ()
    {
        var self = this;
        this.collection = new Collections.Distributions();
        this.collection.fetch({success: function() {
            self.view = new Views.DistributionsView(self.collection);
            self.view.render();
        }});
    },

    render_systems: function ()
    {
      if (!this.systems)
      {
        console.log('Render systems');
        this.systems = new Views.SystemsView();
      } else {
        this.systems.render();
      }
    },

    render_system: function (id)
    {
        var self = this;
        this.model = new Models.System({id: id});
        this.model.fetch({success: function(){
            self.view = new Views.SystemView(self.model);
            self.view.render();
        }});
    },

    routes: {"": "render_dashboard",
        "settings/distributions": "render_settings_distributions",
        "settings/distribution/:name": "render_settings_distribution",
        "systems": "render_systems",
        "system/:id": "render_system"},

    user: User
});
