var Views = Views || { };

Views.SystemsView =  Backbone.View.extend({

  initialize: function () {
    this.collection = new Collections.Systems();
    this.collection.bind('refresh', this.render);
    Apiary.set_title("Systems");
    Apiary.load_template("pages/systems", this);
  },

  bind_toolbar: function(self) {
    console.debug('On toolbar');
  },

  get_data: function() {
    var self = this;
    this.collection.fetch(
        {success: function(collection) {
          self.on_data(collection);
        },
          error: function(coll, res) {
            if (res.status === 404) {
              // TODO: handle 404 Not Found
            } else if (res.status === 500) {
              // TODO: handle 500 Internal Server Error
            }
          }
        });
  },


  on_data: function(collection)
  {
    this.render();
  },

  render: function()
  {
    console.log('Rendering');
    Apiary.set_content(this.template);
    var table = $("#items");
    table.hide();
    table.find('tbody').render(this.collection.toJSON(),
                 {
                   icons: {
                     html: function() {
                       var icons = '';
                       if ( this.provision === true )
                       {
                         icons = icons + '<i class="icon icon-warning icon-flag"></i> ';
                       }
                       var icon = Math.floor((Math.random()*10)+1);
                       if ( icon <= 4 )
                         icons = icons + '<i class="icon icon-success icon-thumbs_up"></i> ';
                       if ( icon === 5 )
                         icons = icons + '<i class="icon icon-danger icon-fire"></i> ';
                       if ( icon === 6 )
                         icons = icons + '<i class="icon icon-skull"></i> ';
                       if ( icon === 7 )
                         icons = icons + '<i class="icon icon-success icon-hdd"></i> ';
                       if ( ( icon === 8 ) &&  ( this.provision === false ) )
                         icons = icons + '<i class="icon icon-warning icon-flag"></i> ';
                       if ( ( icon === 9 ) &&  ( this.provision === false ) )
                         icons = icons + '<i class="icon icon-warning icon-cogwheel"></i> ';
                       if ( icon === 10 )
                         icons = icons + '<i class="icon icon-information icon-moon"></i> ';

                       return icons;
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
                   system: {
                     href: function () {
                       return "#system/" + this.id;
                     },
                     text: function () {
                       return this.id;
                     }
                   }
                 });
    console.log('Post rendering, binding');
    ViewTools.add_tablesorter(table);
    ViewTools.bind_select_column(table);
    ViewTools.init_tooltips();
    table.show();
  },

  on_template: function (self, html) {
    self.template = html;
    self.get_data();
  },

  template: null
});
