var Collections = Collections || { };

Collections.Distributions = Backbone.Collection.extend({url: '/api/distributions', model: Models.Distribution});
