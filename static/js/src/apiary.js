Transparency.matcher = function(element, key) {
  return element.getAttribute('data-bind') === key;
};

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
