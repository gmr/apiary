define(
  "apiary",
  ["jquery",
   "backbone",
   "router",
   "view_tools"],
  function($, backbone, Router, ViewTools) {
    function Apiary()
    {
      this.dispatcher = _.clone(Backbone.Events);

      this.view_tools = ViewTools();

      if( 'localStorage' in window && window['localStorage'] !== null )
      {
        this.storage = window.localStorage;
      } else {
        this.storage = null;
      }

      this.get_item = function(key)
      {
        if ( this.storage !== null )
        {
          var json_value = this.storage.getItem(key);
          if ( json_value !== null )
          {
            return JSON.parse(json_value).pop(0);
          }
        }
        return null;
      };

      this.router = new Router(this);

      this.set_item = function(key, value)
      {
        if ( this.storage !== null )
        {
          this.storage.setItem(key, JSON.stringify([value]));
        }
      };
    }
    return Apiary;
  }
);
