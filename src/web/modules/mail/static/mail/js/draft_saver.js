$(document).ready(
    function()
    {
        function get_mail_data_to_post()
        {
            var $form = $('#mail-composer')
            var form_data = $form.serializeArray()
            var post_data = {}
            for (var i = 0; i < form_data.length; i++)
                post_data[form_data[i].name] = form_data[i].value
            return post_data
        }

        function save_current_email_data()
        {
            $.post('../save/', get_mail_data_to_post())
        }

        // Draft saving interval in milliseconds
        const SAVING_INTERVAL =  3000

        var timer = setInterval(save_current_email_data, SAVING_INTERVAL)
    }
)