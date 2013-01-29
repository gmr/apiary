define([
    'underscore',
    'backbone'
], function(_, Backbone) {
    var Distribution = Backbone.Model.extend({url: '/api/distribution', idAttribute: "name"});
    return Distribution;
});
