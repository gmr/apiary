define(
  "views/system",
  ["jquery",
    "backbone",
    "view_tools"],
  function($, backbone, ViewTools) {
      return Backbone.View.extend({
        initialize: function (model) {
          this.model = model;
          this.model.bind('refresh', this.render);
          self.template = ViewTools.setup_page("system");
        },
        table: null
    });
  });
