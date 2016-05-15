/* Plugin initializers */
$(document).ready(function() {
    $('.datetimepicker').each(function(_, datetimepicker) {
        var $datetimepicker = $(datetimepicker);
        var format = $datetimepicker.data('format') || 'DD.MM.YYYY';
        var view_mode = $datetimepicker.data('view-mode') || 'days';
        var pick_time = ($datetimepicker.data('pick-time') || 'true') === 'true';

        /* TODO: minDate and maxDate */
        $datetimepicker.datetimepicker({
            format: format,
            viewMode: view_mode,
            pickTime: false
        })
    })
});