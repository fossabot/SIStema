$(document).ready(function () {
    var button = $('#check_all');
    var group_name = button.attr('checkbox_for');
    $('#delete_all').hide().click(
        function () {
            if (number_of_checked(group_name) > 0) {
                $('#dialog').modal({});
            }
        }
    );

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
    })
});