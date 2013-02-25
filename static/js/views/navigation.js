define(
  "views/navigation",
  ["jquery",
   "backbone",
   "view_tools"],
  function($, Backbone, ViewTools) {
    return Backbone.View.extend({
       initialize: function (router) {
         this.el = $('#navbar').find('div.container-fluid');
         this.router = router;
         var tools = new ViewTools();
         this.template = tools.get_template('snippets/navigation');
       },
       render: function() {
         var _this = this;
         this.template.done(function(html){
           _this.el.html(html).render({user: _this.router.user.profile});
         });
       }
     });
});
