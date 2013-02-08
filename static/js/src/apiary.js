Transparency.matcher = function(element, key) {
  return element.getAttribute('data-bind') === key;
};

var Router = Backbone.Router.extend({

  initialize: function()
  {
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
    var self = this;
    this.collection = new Collections.Systems();
    this.collection.fetch({success: function() {
        self.view = new Views.SystemsView(self.collection);
        self.view.render();
    }});
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

var Apiary = {

  dispatcher: _.clone(Backbone.Events),

  get_template: function(path)
  {
    return Apiary.templates[path];
  },

  initialize: function() {
    document.router = new Router();
    Backbone.history.start();
  },

  load_template: function(path, context)
  {
    var self = this;
    if ( self.templates.hasOwnProperty(path) )
    {
      context.on_template(context, self.templates[path]);
    } else {
      $.get("/static/templates/" + path + ".html?req=" + (new Date()).getTime(),
        function(html)
        {
          self.templates[path] = html;
          context.on_template(context, html);
        });
    }
  },

  set_active_navbar_item: function(href) {
    var navbar = $("#navbar");
    navbar.find('li.active').removeClass('active');
    navbar.find('a[href="' + href + '"]').parent('li').addClass('active');
  },

  set_content: function(html)
  {
    $('#content').html(html);
  },

  set_title: function(title) {
    $("title").html('Apiary &ndash; ' + title);
  },

  templates: {}
};
