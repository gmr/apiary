define(
    "models/distribution",
    ["backbone"],
    function(Backbone) {
      return Backbone.Model.extend({url: '/api/distribution',
                                    idAttribute: "name"});
    }
);
