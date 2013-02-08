var Views = Views || { };

Views.SystemView =  Backbone.View.extend({

    initialize: function (model) {
        this.model = model;
        this.model.bind('refresh', this.render);
    },

    on_template: function (self, html) {
        Apiary.set_content(html);
        Apiary.set_title("System " + this.model.id);
        $("#content").render(self.model.toJSON());
        $('.has-tooltip').tooltip();
    },

    render: function () {
        Apiary.load_template("pages/system", this);
    },

    table: null
});
