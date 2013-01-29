/**
 * Apiary JavaScript toolkit
 */
define([
    "jquery",
    "underscore",
    "backbone",
    "dust",
    "dust-helpers",
    "bootstrap"
], function($, _, Backbone, dust, dust_helpers, bootstrap) {
    var ApiaryTools = {

        set_active_navbar_item: function(href) {
            var navbar = $("#navbar");
            navbar.find('li.active').removeClass('active');
            navbar.find('a[href="' + href + '"]').parent('li').addClass('active');
        },

        set_title: function(title) {
            $("title").html('Apiary &ndash; ' + title);
        },

        compile_template: function()
        {
            if ( ApiaryTools.uncompiled_templates.length > 0 )
            {
                var path = ApiaryTools.uncompiled_templates.shift();
                $.get("/static/templates/" + path + ".dust?req=" + (new Date()).getTime(), function(html)
                {
                    //console.log('Compiling ' + path);
                    var compiled = dust.compile(html, path);
                    dust.loadSource(compiled);
                    ApiaryTools.compile_template();
                });
            } else {
                ApiaryTools.dispatcher.trigger("dust:compilation_complete");
            }
        },

        compile_templates: function(paths)
        {
            this.uncompiled_templates = paths;
            ApiaryTools.compile_template();
        },

        dispatcher: _.clone(Backbone.Events),

        render_template: function(path, data, callback)
        {
            dust.render(path, data, function(err, rendered)
            {
                if ( err !== null )
                {
                    console.log("Error rendering " + path + ": " + err);
                } else {
                    callback(rendered);
                }
            });
        },
        uncompiled_templates: []
    };

    return ApiaryTools;
});
