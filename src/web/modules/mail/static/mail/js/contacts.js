$(document).ready(function () {
    var button = $('#check_all');
    var group_name = button.attr('checkbox_for');
    $('.contact-item').click(
        function () {
            var name = $('#' + this.id + ' .contact_name').text();
            var email = $('#' + this.id + ' .contact_email').text();
            $('#id_display_name').val(name);
            $('#id_email').val(email);
            $('#save_contact').val('Изменить');
        }
    );
    $('#id_email').keyup(function () {
        $('#save_contact').val('Сохранить');
    });

     button.click(function () {
        change_checked(group_name, $(this).prop('checked'));
        if ($(this).prop('checked')) {
            $('label[for="' + this.id + '"]').html('Снять выделение');
            $('#delete_all').show();
        }
        else {
            $('label[for="' + this.id + '"]').html('Выделить все');
            $('#delete_all').hide();
        }
    });

    $('input:checkbox[checkbox_group="' + group_name + '"]').click(function () {
        console.log($(this).prop('checked'), number_of_checked(group_name));
        if (number_of_checked(group_name) > 0)
            $('#delete_all').show();
        else
            $('#delete_all').hide();
    });

    $('#delete_all').hide().click(function () {

    })
});