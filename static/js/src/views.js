var ViewTools = {

  add_pagination: function(table) {
    var url = '/static/templates/snippets/pagination.html?req=' + (new Date()).getTime();
    $.get(url, function(html) {
      $('.pagination').html(html);

    });
  },

  add_tablesorter: function (table) {


    console.log('Adding tablesorter');
    console.log(table);



    $.extend($.tablesorter.themes.bootstrap, {
      // these classes are added to the table. To see other table classes available,
      // look here: http://twitter.github.com/bootstrap/base-css.html#tables
      table      : 'table table-hover table-zebra table-bordered table-condensed',
      footerRow  : '',
      footerCells: '',
      icons      : '', // add "icon-white" to make them white; this icon class is added to the <i> in the header
      sortNone   : '',
      sortAsc    : 'icon-up_arrow',
      sortDesc   : 'icon-down_arrow',
      active     : '', // applied when column is sorted
      hover      : '', // use custom css here - bootstrap class may not override it
      filterRow  : '', // filter row class
      even       : '', // odd row zebra striping
      odd        : ''  // even row zebra striping
    });


    table.tablesorter({sortList: [[1, 0]],
                        headers: {0: {sorter: false}},
                        theme : "bootstrap", // this will
                        widthFixed: true,
                        headerTemplate : '{content} {icon}', // new in v2.7. Needed to add the bootstrap icon!
                        widgets : [ "uitheme", "zebra" ],
                        widgetOptions : {
                          zebra : ["even", "odd"]
                        }});
    table.tablesorterPager({container: $(".pager"), output: '{startRow} to {endRow} of {totalRows}'});
    // Hack to overwrite tablesorter's hijack of the cell
    table.find("thead > tr > th:first-child").html('<i class="icon icon-unchecked"></i>');
  },

  add_toolbar: function(context) {
    $.get('/static/templates/snippets/toolbar.html?1', function(html) {
      $('.toolbar').html(html);
      context.bind_toolbar();
    });
  },

  bind_select_column: function (table) {
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
  },

  init_tooltips: function() {
    $('[rel="tooltip"]').tooltip({ container : 'body' });
  }

};
