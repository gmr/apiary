define(
    "models/system",
    ["backbone"],
    function(Backbone) {
      return Backbone.Model.extend({url: '/api/system',
                                     idAttribute: "uid"});
    }
);
