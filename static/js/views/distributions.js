var Views = Views || { };

Views.DistributionsView =  Backbone.View.extend({
  add_tablesorter: function () {
    this.table.tablesorter({cssAsc: "table-sort-asc",
                             cssDesc: "table-sort-desc",
                             sortList: [[1, 0]],
                             headers: {0: {sorter: false}}});
  },
  bind_select_column: function () {
    var tbody = this.table.find('tbody');
    var header = this.table.find("thead tr:first th:first");
    var delete_button = $("#btn-delete");
    header.click(function () {
      var checked = header.find("i.icon-check");
      if (checked.length > 0) {
        checked.addClass("icon-unchecked").removeClass("icon-check");
        tbody.find("tr > td:first-child > i.icon-check").addClass("icon-unchecked").removeClass("icon-check");
        delete_button.addClass("disabled");
      } else {
        header.find("i").addClass("icon-check").removeClass("icon-unchecked");
        tbody.find("tr > td:first-child > i.icon-unchecked").addClass("icon-check").removeClass("icon-unchecked");
        delete_button.removeClass("disabled");
      }
    });

    var columns = tbody.find("tr > td:first-child");
    columns.click(function () {
      var checked = $(this).find("i.icon-check");
      if (checked.length > 0) {
        checked.addClass("icon-unchecked").removeClass("icon-check");
        if (columns.find("i.icon-check").length === 0) {
          delete_button.addClass("disabled");
        }
      } else {
        $(this).find("i").addClass("icon-check").removeClass("icon-unchecked");
        delete_button.removeClass("disabled");
      }
    });
  },

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
    self.bind_select_column();
    self.add_tablesorter();
  },

  render: function () {
    Apiary.load_template("pages/distributions", this);
  },

  table: null
});
