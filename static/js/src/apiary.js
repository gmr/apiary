Transparency.matcher = function(element, key) {
  return element.getAttribute('data-bind') === key;
};

var Router = Backbone.Router.extend({routes: {"": "render_dashboard",
                                     "settings/distributions": "render_settings_distributions",
                                     "settings/distribution/:id": "render_settings_distribution"},
                                     render_dashboard: function()
                                     {

                                       //Apiary.render_template("pages/dashboard", {user: User}, render_page);
                                       //Apiary.set_active_navbar_item("");
                                     },

                                     render_settings_distributions: function ()
                                     {
                                       if (!this.distributions_view) {
                                         this.distributions_view = new Views.DistributionsView();
                                       }
                                       this.distributions_view.render();
                                     },
                                     user: null,
                                     initialize: function()
                                     {
                                       if (!this.navigation_view) {
                                         this.navigation_view = new Views.NavigationView();
                                       }
                                     }
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
    this.user = User;
    this.user.initialize();
  },

  load_template: function(path, context)
  {
    if ( Apiary.templates.hasOwnProperty(path) )
    {
      callback(Apiary.templates[path]);
    } else {
      $.get("/static/templates/" + path + ".html?req=" + (new Date()).getTime(),
            function(html)
            {
              Apiary.templates[path] = html;
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
