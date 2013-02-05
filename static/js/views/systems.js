var Views = Views || { };

Views.SystemsView =  Backbone.View.extend({

  initialize: function () {
    this.collection = new Collections.Systems();
    var self = this;
    this.collection.fetch({success: function () {
      self.render();
    }});
  },

  on_template: function (self, html) {
    Apiary.set_content(html);
    self.table = $('#systems');
    var tbody = self.table.find('tbody');
    var values = self.collection.toJSON();
    tbody.render(values, {system: {
                            href: function () {
                              return "#system/" + this.id;
                            },
                            text: function () {
                              return this.id;
                            }
                          },
                          linked_profile: {
                              href: function () {
                                return "#settings/profile/" + this.profile;
                              },
                              text: function () {
                                return this.profile;
                              }
                          },
                          icons: {
                            html: function() {
                              icons = '';
                              if ( this.provision === true )
                              {
                                icons = icons + '<i class="icon icon-flag icon-error"></i>';
                              }
                              return icons;
                            }
                          }
                        });
    Apiary.set_title("Systems");
    ViewTools.add_pagination(this);
    //ViewTools.add_tablesorter(this.table);
    ViewTools.add_toolbar(this);
    ViewTools.bind_select_column(this.table);
  },

  bind_toolbar: function(self) {
    console.debug('On toolbar');
  },

  render: function () {
    Apiary.load_template("pages/systems", this);
  },

  table: null
});
