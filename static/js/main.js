// Apiary JavaScript

require.config({
    paths: {
        jquery: 'libs/jquery/jquery.min',
        underscore: 'libs/underscore/underscore.min',
        backbone: 'libs/backbone/backbone.min',
        knockback: 'libs/knockback/knockback.min',
        knockout: 'libs/knockout/knockout.min'
    }
});

require ([
    'app'
], function(App) {
    return App.initialize();
});
