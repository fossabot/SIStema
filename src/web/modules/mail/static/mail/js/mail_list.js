$(document).ready(function () {
    var button = $('#check_all');
    var group_name = button.attr('checkbox_for');
    var not_read = $('#not_read_button');
    $('#delete_all').hide().click(
        function () {
            if (number_of_checked(group_name) > 0) {
                $('#dialog').modal({});
            }
        }
    );

    var val = not_read.val().toLowerCase();
    val = val != 'false';

    $('#not_read').prop('checked', val);

    button.click(function () {
        change_checked(group_name, $(this).prop('checked'));
        if ($(this).prop('checked')) {
            $('label[for="' + this.id + '"]').html('Снять выделение');
            $('#delete_all').show();
        }
        else
            $('label[for="' + this.id + '"]').html('Выделить все');
    });

    $('input:checkbox[checkbox_group="' + group_name + '"]').click(function () {
        if (number_of_checked(group_name) > 0)
            $('#delete_all').show();
        else
            $('#delete_all').hide();
    });

    $('.read').click(function () {
        $(this).removeClass('read');
    });

    not_read.click(
        function () {
            val = !val;
            not_read.val(val);
            $('#not_read').prop('checked', val);
        }
    );
});