define(
    "collections/systems",
    ["backbone",
     "models/system"],
  function(Backbone, System) {
    return Backbone.Collection.extend({
      url: '/api/systems',
      initialize: function() {
        this.deferred = this.fetch();
      },
      model: System
    });
  });
