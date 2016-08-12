$(document).ready(
    function () {
        function get_mail_data_to_post($form) {
            var form_data = $form.serializeArray();
            var post_data = {};
            for (var i = 0; i < form_data.length; i++)
                post_data[form_data[i].name] = form_data[i].value;
            return post_data
        }

        function get_submit_url($form) {
            return $form.data('submit-url')
        }

        function save_current_email_data($form) {
            $.post(get_submit_url($form), get_mail_data_to_post($form))
        }

        // Draft saving interval in milliseconds
        const SAVING_INTERVAL = 3000;

        var $form = $('#mail-composer');
        var timer = setInterval(save_current_email_data, SAVING_INTERVAL, $form)
    }
);