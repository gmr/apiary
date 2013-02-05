// 3rd Party Libraries
// @codekit-prepend "libs/jquery/jquery.min.js"
// @codekit-prepend "libs/jquery.tablesorter/jquery.tablesorter.min.js"
// @codekit-prepend "libs/transparency/transparency.min.js"
// @codekit-prepend "libs/underscore/underscore.min.js"
// @codekit-prepend "libs/backbone/backbone.min.js"
// @codekit-prepend "libs/bootstrap/bootstrap.min.js"


// View Support Tools

// Internal views, models and collections
// @codekit-append "models/distribution.js"
// @codekit-append "models/system.js"
// @codekit-append "collections/distributions.js"
// @codekit-append "collections/systems.js"
// @codekit-append "views/distributions.js"
// @codekit-append "views/systems.js"
// @codekit-append "views/navigation.js"

// @codekit-append "src/user.js"
// @codekit-append "src/views.js"
// @codekit-append "src/apiary.js"

jQuery(document).ready(function($) {
    Apiary.initialize();
});
