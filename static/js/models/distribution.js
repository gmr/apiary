var Models = Models || { };

Models.Distribution = Backbone.Model.extend({url: '/api/distribution',
                                             idAttribute: "name"});
