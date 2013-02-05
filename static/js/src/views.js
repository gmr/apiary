var ViewTools = {

  add_pagination: function() {
    $.get('/static/templates/snippets/pagination.html', function(html) {
      $('.pagination').html(html);
    });
  },

  add_tablesorter: function (table) {
    table.tablesorter({cssAsc: 'table-sort-asc',
                       cssDesc: 'table-sort-desc',
                       sortList: [[1, 0]],
                       headers: {0: {sorter: false}}});
  },

  add_toolbar: function(context) {
    $.get('/static/templates/snippets/toolbar.html', function(html) {
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
  }

};
