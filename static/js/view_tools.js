define(
  "view_tools",
  ["jquery",
   "underscore",
   "jquery.tablesorter",
   "jquery.tablesorter.pager",
   "jquery.tablesorter.widgets",
   "bootstrap"],
  function($, _) {
    function ViewTools()
    {
      this.apply_snippet = function(workspace, snippets, promise)
      {
        if ( snippets.length == 0 )
        {
          var value = workspace.html();
          workspace.remove();
          promise.resolve(value);
          return;
        }
        var _this = this;
        var snippet = snippets.shift();
        var template = this.get_template('snippets/' + snippet.filename);
        template.done(function(template){
          "use strict";
          workspace.find(snippet.context).html(template);
          _this.apply_snippet(workspace, snippets, promise);
        });
      };

      this.apply_snippets = function(value, snippets)
      {
        $('body').append('<div id="apply-snippets" class="hidden"></div>');
        var workspace = $('#apply-snippets');
        var promise = $.Deferred();
        workspace.html(value);
        this.apply_snippet(workspace, snippets, promise);
        return promise;
      };

      this.add_tablesorter = function (table) {
        // Get the current page and the number of items to show per page
        var current_page = document.apiary.get_item('pagination:' + table[0].id + ':current_page');
        if ( current_page === null )
        {
          current_page = 0;
        }
        var items_per_page = document.apiary.get_item('pagination:items_per_page');
        if ( items_per_page === null )
        {
          items_per_page = 10;
        }

        // Extend the tablesorter theme for the Bootstrap implementation
        $.extend($.tablesorter.themes.bootstrap, {
          table      : 'table table-hover table-zebra table-bordered table-condensed',
          footerRow  : '',
          footerCells: '',
          icons      : '',
          sortNone   : '',
          sortAsc    : 'icon-up_arrow',
          sortDesc   : 'icon-down_arrow',
          active     : '',
          hover      : '',
          filterRow  : '',
          even       : '',
          odd        : ''
        });

        // Apply the tablesorter
        table.tablesorter({sortList: [[1, 0]],
                           headers: {0: {sorter: false}},
                           theme : "bootstrap",
                           widthFixed: true,
                           headerTemplate : '{content} {icon}',
                           widgets : [ "uitheme", "zebra" ],
                           widgetOptions : {
                             zebra : ["even", "odd"]
                           }});

        // Apply the pager
        table.tablesorterPager({container: $(".pager"),
                                output: this.pager_output().replace('{size}', items_per_page),
                                page: current_page,
                                size: items_per_page});
        var _this = this;
        table.bind('pagerComplete pageMoved', function(e, c) {
          var items = c.endRow - c.startRow + 1;
          _.each($('.pagedisplay'), function(item){
            var ref = $(item);
            ref.html(ref.html().replace('{count}', items));
          });
        });

        // Hack to overwrite tablesorter's hijack of the cell
        table.find("thead > tr > th:first-child").html('<i class="icon icon-unchecked"></i>');
        this.bind_pagination(table);
        // Hack because setting size doesn't seem to work
        $('.pagination').find('select.pagesize').val(items_per_page).trigger('change');
      };

      this.alert_timeout = null;

      this.bind_pagination = function(table) {
        var _this = this;
        var page_size = $('div.pagination').find('select.pagesize');
        page_size.change(function(){
          document.apiary.set_item('pagination:items_per_page', this.value);
        });
        table.bind('pagerChange', function(e,c){
          document.apiary.set_item('pagination:' + table[0].id + ':current_page', c.page);
          c.output = _this.pager_output().replace('{size}', c.size);
        });
      };

      this.bind_select_column = function (table) {
        var tbody = $(table).find('tbody');
        var header = $(table).find('thead tr:first th:first');
        var delete_button = $('#btn-delete');
        header.click(function () {
            var checked = header.find('i.icon-check');
            if (checked.length > 0) {
                checked.addClass('icon-unchecked').removeClass('icon-check');
                tbody.find('tr > td:first-child > i.icon-check').addClass('icon-unchecked').removeClass('icon-check');
                delete_button.addClass('disabled');
            } else {
                header.find('i').addClass('icon-check').removeClass('icon-unchecked');
                tbody.find('tr > td:first-child > i.icon-unchecked').addClass('icon-check').removeClass('icon-unchecked');
                delete_button.removeClass('disabled');
            }
        });

        var columns = tbody.find('tr > td:first-child');
        columns.click(function () {
            var checked = $(this).find('i.icon-check');
            if (checked.length > 0) {
                checked.addClass('icon-unchecked').removeClass('icon-check');
                if (columns.find('i.icon-check').length === 0) {
                    delete_button.addClass('disabled');
                }
            } else {
                $(this).find('i').addClass('icon-check').removeClass('icon-unchecked');
                delete_button.removeClass('disabled');
            }
        });
      };

      this.destroy_alerts = function() {
        $('.alert').remove();
      };

      this.destroy_tooltips = function() {
        $('.tooltip').hide();
        $('[rel="tooltip"]').tooltip('destroy');
      };

      this.get_template = function(path)
      {
        if ( this.templates.hasOwnProperty(path) )
        {
          var promise = $.Deferred();
          promise.resolve(this.templates[path]);
          return promise;
        }
        var _this = this;
        return $.get("/static/templates/" + path + ".html?req=" + (new Date()).getTime()).then(
            function(data){
              _this.templates[path] = data;
              return data;
            },
            function(data){
              console.log("Error fetching template for " + path);
            });
      };

      this.hide_loading = function() {
        $('#loading').toggle();
      };

      this.init_alerts = function() {
        $(".alert").alert();
      };

      this.init_tooltips = function() {
        $('[rel="tooltip"]').tooltip({ container : 'body' });
      };

      this.initialize = function() {
        this.show_loading();
      };

      this.reset_ui = function()
      {
        this.destroy_alerts();
        this.destroy_tooltips();
        if ( this.alert_timeout )
        {
          clearTimeout(this.alert_timeout);
        }
      };

      this.restore_settings = function(table) {
      };

      this.set_active_navbar_item = function(href) {
        var navbar = $("#navbar");
        navbar.find('li.active').removeClass('active');
        navbar.find('a[href="' + href + '"]').parent('li').addClass('active');
      };

      this.show_loading = function(context) {
        this.reset_ui();
        if (context === undefined)
        {
          context = $('#content');
        }
        this.get_template('snippets/loading').done(function(html){
          context.html(html);
        });
      };

      this.start_alert_dismiss_timer = function() {
        var _this = this;
        this.alert_timeout = setTimeout(function(){
          $('.alert').fadeOut();
          _this.alert_timeout = null;
        }, 10000);
      };

      this.pager_output = function() {
        var output = $('#pager-output-nofilter').html();
        if (output === null)
        {
          return 'Page {page} of {totalPages}';
        }
        return output;
      };

      this.set_content = function(html) {
        $('#content').html(html);
      };

      this.set_title = function(title) {
        $("title").html('Apiary &ndash; ' + title);
      };

      this.setup_page = function(context, value)
      {
        this.show_loading();
        this.set_title(context.title);
        this.set_breadcrumb(context.title, value);
        if ( context.snippets !== undefined )
        {
          var promise = $.Deferred();
          var _this = this;
          this.get_template('pages/' + context.title.toLowerCase()).done(function(html){
            _this.apply_snippets(html, context.snippets).done(function(html){
              promise.resolve(html.replace(/{item}/g, context.title));
            });
          });
          return promise;
        }
        return this.get_template('pages/' + context.title.toLowerCase());
      };

      this.templates = {};

      this.set_breadcrumb = function(title, value) {
        this.get_template('breadcrumbs/' + title.toLowerCase()).done(function(html){
          if ( value === undefined )
          {
              $("#breadcrumbs").html(html);
          } else {
            $("#breadcrumbs").html(html.replace('{value}', value));
          }
        });
      };
    }
    return ViewTools;
  }
);
