var Views = Views || { };

Views.DistributionsView =  Backbone.View.extend({

  initialize: function () {
    this.collection = new Collections.Distributions();
    var self = this;
    this.collection.fetch({success: function () {
      self.render();
    }});
  },

  on_template: function (self, html) {
    Apiary.set_content(html);
    self.table = $('#distributions');
    var tbody = self.table.find('tbody');
    var values = self.collection.toJSON();
    tbody.render(values, {
      distribution: {
        href: function () {
          return "#settings/distribution/" + this.name;
        },
        text: function () {
          return this.name;
        }
      }
    });
    Apiary.set_title("Distributions");
    ViewTools.bind_select_column(self.table);
    ViewTools.add_tablesorter(self.table);
  },

  render: function () {
    Apiary.load_template("pages/distributions", this);
  },

  table: null
});
