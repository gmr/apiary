define(
  "user",
  ["jquery"],
  function($) {

    function User()
    {
      this.authenticated = false;
      this.profile = {};

      var profile = $.get('/profile').then(
          function(data){
            return data;
          },
          function(data) {
            return null;
          });

      this.authenticate = function() {
        var deferred = $.Deferred();
        profile.done(function(data){
          var _this = this;
          if ( data !== undefined )
          {
            _this.authenticated = true;
            _this.profile = data;
          } else {
            _this.authenticated = false;
            _this.profile = {};
          }
          deferred.resolve(_this);
        });
        return deferred;
      };



    }
    return User;
  }
);
