$(document).ready(function(){
    $('.table-panel .table-filter').change(function(){
        var $table_panel = $(this).closest('.table-panel');
        var table_name = $table_panel.data('table-name');
        var table_identifiers = $table_panel.data('table-identifiers');
        var filter = $(this).val();

        var url = '/frontend/table/' + table_name + '/data/?filter=' + encodeURIComponent(filter) + '&' + $.param(table_identifiers)
        $.getJSON(url,
            function(data) {
                var rows = data.rows;
                var $table = $table_panel.find('table tbody');
                $table.find('tr:not(:first-child)').remove();
                $.each(rows, function(row_idx, row) {
                    var $tr = $('<tr>');
                    $.each(row, function(column_idx, column) {
                        var $td = $('<td>').html(column);
                        $tr.append($td);
                    });
                    $table.append($tr);
                });
            })
    });
});