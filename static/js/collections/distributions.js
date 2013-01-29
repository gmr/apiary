define([
    'backbone',
    'models/distribution'
], function(Backbone, Distribution) {
    return Backbone.Collection.extend({url: '/api/distributions', model: Distribution});
});

