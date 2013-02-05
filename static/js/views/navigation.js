var Views = Views || { };

Views.NavigationView = Backbone.View.extend({
      on_template: function (context, html) {
        $("#navbar").render(html, {user: document.router.user});
      },
      render: function () {
        Apiary.load_template("snippets/navigation", this);
      }
    });
