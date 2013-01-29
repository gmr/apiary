
define([
    "jquery",
    "underscore",
    "backbone",
    "dust",
    "apiary_tools",
    "collections/distributions",
    "user"
], function($, _, backbone, dust, ApiaryTools, DistributionCollection, User) {
    var DistributionsView = {

        delete_button: $("#btn-delete"),
        table: $("#distribution-table"),

        add_tablesorter: function() {
            DistributionsView.table.tablesorter({
                cssAsc: "table-sort-asc",
                cssDesc: "table-sort-desc",
                sortList: [[1, 0]],
                headers: {0: {sorter: false}}});
        },

        bind_select_column: function() {
            var header = this.table.find("thead tr:first th:first");
            header.click(function(){
                var checked = header.find("i.icon-check");
                if ( checked.length > 0 )
                {
                    checked.addClass("icon-unchecked").removeClass("icon-check");
                    DistributionsView.table.find("tbody tr td:first i.icon-check").addClass("icon-unchecked").removeClass("icon-check");
                    DistributionsView.delete_button.addClass("disabled");
                } else {
                    header.find("i").addClass("icon-check").removeClass("icon-unchecked");
                    DistributionsView.table.find("tbody tr td:first i.icon-unchecked").addClass("icon-check").removeClass("icon-unchecked");
                    DistributionsView.delete_button.removeClass("disabled");
                }
            });

            var columns = DistributionsView.table.find("tbody tr td:first");
            columns.click(function(){
                var checked = $(this).find("i.icon-check");
                if ( checked.length > 0 )
                {
                    checked.addClass("icon-unchecked").removeClass("icon-check");
                    if ( columns.find("i.icon-check").length === 0 )
                    {
                        DistributionsView.delete_button.addClass("disabled");
                    }
                } else {
                    $(this).find("i").addClass("icon-check").removeClass("icon-unchecked");
                    DistributionsView.delete_button.removeClass("disabled");
                }
            });
        },

        initialize: function() {
            this.table = new DistributionsView.Table();
        },

        Table: Backbone.View.extend({

            columns: [{name: "name", label: "Name", link: "#settings/distribution/:name", center: false},
                      {name: "version", label: "Version", center: true},
                      {name: "breed", label: "Breed", center: true},
                      {name: "architecture", label: "Architecture", center: true},
                      {name: "profile_count", label: "Profiles",  center: true}],

            initialize: function() {
                if (!this.collection) {
                    this.collection = new DistributionCollection();
                }
                var self = this;
                this.collection.fetch({
                    success: function (data_unused) {
                        self.render();
                    }
                });
            },

            on_rendered: function(content) {
                $("#content").html(content);
            },

            render:function() {
                ApiaryTools.render_template("components/tableview",
                                            {breadcrumbs: [{name: "Settings", path: "#settings"},
                                                           {name: "Distributions", path: "#settings/distributions"}],
                                             headers: this.headers,
                                             columns: this.columns,
                                             data: this.collection.toJSON()},
                                            this.on_rendered);
                ApiaryTools.set_title("Distributions");
            },

            tagName: "tbody"
        })
    };

    return DistributionsView;
});
