
var Distribution = Backbone.Model.extend({url: '/api/distribution', idAttribute: "name"});
var DistributionCollection = Backbone.Collection.extend({url: '/api/distributions', model: Distribution});

var DistributionsTableView = {

    table: $('#distribution-table'),

    add_tablesorter: function() {
        DistributionsTableView.table.tablesorter({
            cssAsc: "table-sort-asc",
            cssDesc: "table-sort-desc",
            sortList: [[1, 0]],
            headers: {0: {sorter: false}}});
    },

    bind_select_column: function() {
        var header = this.table.find('thead tr:first th:first');
        header.click(function(){
            var checked = header.find('i.icon-check');
            if ( checked.length > 0 )
            {
                checked.addClass('icon-unchecked').removeClass('icon-check');
                DistributionsTableView.table.find('tbody tr td:first i.icon-check').addClass('icon-unchecked').removeClass('icon-check');
            } else {
                header.find('i').addClass('icon-check').removeClass('icon-unchecked');
                DistributionsTableView.table.find('tbody tr td:first i.icon-unchecked').addClass('icon-check').removeClass('icon-unchecked');
            }
        });

        var columns = DistributionsTableView.table.find('tbody tr td:first');
        console.debug(columns);
        columns.click(function(){
            console.log(this);
            var checked = $(this).find('i.icon-check');
            if ( checked.length > 0 )
            {
                checked.addClass('icon-unchecked').removeClass('icon-check');
            } else {
                $(this).find('i').addClass('icon-check').removeClass('icon-unchecked');
            }
        });
    },

    initialize: function() {
        this.table = new DistributionsTableView.Table();
    },

    Row: Backbone.View.extend({
        tagName:'tr',
        initialize: function() {
            if ( $('#distribution-table').length > 0 )
            {
                this.template = _.template($('#item-template').html());
            }
        },
        render:function () {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        }
    }),

    Table: Backbone.View.extend({
        initialize: function() {
            this.el = DistributionsTableView.table.find('> tbody');
            if (!this.collection) {
                this.collection = new DistributionCollection();
            }
            var self = this;
            this.collection.fetch({
                success: function (data_unused) {
                    self.render();
                    DistributionsTableView.add_tablesorter();
                    DistributionsTableView.bind_select_column();
                }
            });
        },

        render:function() {
            $(this.el).empty();
            _.each(this.collection.models, function (distribution) {
                var row = new DistributionsTableView.Row({model:distribution});
                $(this.el).append(row.render().el);
            }, this);
            return this;
        },

        tagName: 'tbody'
    })
};
