var Collections = Collections || { };

Collections.Systems = Backbone.Collection.extend({url: '/api/systems', model: Models.System});
