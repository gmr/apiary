var Views = Views || { };

Views.NavigationView = Backbone.View.extend({

  on_template: function (context, html) {
    $("#navbar").find('div.container-fluid').html(html).render({user: document.router.user.profile});
  },

  render: function () {
    Apiary.load_template("snippets/navigation", this);
  }

});
