define(
  "views/systems",
  ["jquery",
    "backbone",
    "collections/systems"],
  function($, Backbone, Systems) {
    return Backbone.View.extend({

      initialize: function () {
        this.deferred = document.view_tools.setup_page(this);
        this.collection = new Systems();
      },

      bind_icon_legend_close: function() {
        var _this = this;
        $('#table-legend').find('button').click(function(){
          _this.hide_icon_legend();
          document.apiary.set_item('systems:hide_legend', true);
          $('#legend-dismissed').show();
          document.view_tools.start_alert_dismiss_timer();
        });
      },

      bind_toolbar: function() {
        var _this = this;
        $("div.toolbar").find("button > i.icon-refresh").parent("button").click(function(){_this.update_collection();});
      },

      content_area: function() {
        $('#content').find('.row-fluid:nth-child(2)');
      },

      directives: {
        icons: {
          html: function() {
            var icons = '';
            if ( this.provision === true )
            {
              icons = icons + '<i class="icon icon-warning icon-flag"></i> ';
            }
            /*
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
             */
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
      },

      hide_icon_legend: function() {
        var table_legend = $('#table-legend');
        table_legend.hide();
        table_legend.siblings('div.span10').removeClass('span10').addClass('span12');
      },

      render: function()
      {
        var _this = this;
        $.when(this.deferred, this.collection.deferred).then(
          function(template_html, collection)
          {
            document.view_tools.set_content(template_html);
            _this.el = $("#systems");
            _this.el.find('tbody').render(_this.collection.toJSON(), _this.directives);
            document.view_tools.add_tablesorter(_this.el);
            document.view_tools.bind_select_column(_this.el);
            _this.setup_icon_legend();
            _this.bind_toolbar();
          }
        );
      },

      setup_icon_legend: function()
      {
        var hidden = document.apiary.get_item('systems:hide_legend');
        console.log(hidden);
        if ( hidden === null || hidden === false )
        {
          this.bind_icon_legend_close();
        } else {
          this.hide_icon_legend();
        }
      },

      snippets: [{context: '.pagination-top',
                  filename: 'pagination-top'},
                 {context: '.pagination-bottom',
                  filename: 'pagination-bottom'}],

      template: null,

      title: 'Systems',

      update_collection: function()
      {
        document.view_tools.show_loading();
        this.collection.deferred = this.collection.fetch();
        this.render();
      }
    });
  });
