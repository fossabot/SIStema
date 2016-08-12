function get_checked() {
    var checked = [];
    var checkboxes = $('input:checkbox');
    for (var i = 1; i < checkboxes.length; ++i) {
        if ($('#' + checkboxes[i].getAttribute('id')).prop('checked')) {
            checked.push(checkboxes[i].getAttribute('id'));
        }
    }
    return checked
}

$('#delete_all').hide();

$(document).ready(

    function () {
        $('.email-checkbox').click(
            function () {
                if (get_checked().length > 0) {
                    $('#delete_all').show();
                }
                else {
                    $('#delete_all').hide();
                    $('#check_all').prop('checked', false);
                }
            }
        )
        $('#check_all').click(
            function () {
                if ($('#check_all').prop('checked')) {
                    $('input:checkbox').prop('checked', true);
                    $('label[for="check_all"]').html('Снять выделение');
                } else {
                    $('input:checkbox').prop('checked', false);
                    $('label[for="check_all"]').html('Отметить все');
                }
            }
        );

        $('#delete_all').click(
            function () {
                if (get_checked().length > 0) {
                    $('#dialog').modal({});
                }
            }
        );

    }
);