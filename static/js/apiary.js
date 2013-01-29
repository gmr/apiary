define([
    'jquery',
    'collections/distributions',
    'views/distributions'
], function($, DistributionCollection, DistributionsTableView) {
    var initialize = function() {
        //peopleCollection.add([
        //  {name: 'Pepe', lastName: 'Iglesias'},
        //  {name: 'Ronaldinho', lastName: 'Gaullo'}
        //]);
        peopleCollection.add(people_array);
        people_view_model = new DistributionsTableView(DistributionCollection);

        ko.applyBindings(people_view_model);
    }
    return {
        initialize: initialize
    }
});
