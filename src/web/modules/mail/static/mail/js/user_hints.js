$(document).ready
(
    function()
    {
        $('.email-recipient').on('input',
            function()
            {
                console.log('success')
                var $this = $(this);
                var search_value = $this.val();
                var submit_url = $this.data('submit-url');

                $.get(submit_url + '?search=' + encodeURIComponent(search_value), function (data) {
                    $(document).find('.contact-hints').text(data.users);
                },
                'json')
            }
        )
    }
);