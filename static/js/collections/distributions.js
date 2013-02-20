var Collections = Collections || { };

Collections.Distributions = PaginatedCollection.extend({url: '/api/distributions', model: Models.Distribution});
