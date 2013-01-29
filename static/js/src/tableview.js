define([
    "dust"
], function(dust) {

    var TableView = {
        variable_pattern: new RegExp(/\:(\w+)/),

        tableview_column_value: function(chunk, context, bodies, params) {
            var value = params.obj[context.stack.head.name];
            if ( typeof context.stack.head.link !== "undefined" )
            {
                var link = context.stack.head.link;
                do
                {
                    var match = TableView.variable_pattern.exec(link);
                    link = link.replace(match[0], params.obj[match[1]]);
                }  while (TableView.variable_pattern.test(link) === true);
                return chunk.write("<a href=\"" + link + "\">" + value + "</a>");
                } else {
                return chunk.write(value);
            }
        },

        initialize: function(){
            dust.helpers.tableview_column_value = this.tableview_column_value;
        }
    };
    return TableView;
});

// http://localhost:8000/#settings/distributions
