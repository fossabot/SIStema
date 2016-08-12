$(document).ready(
    function () {
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
        })
    }
);