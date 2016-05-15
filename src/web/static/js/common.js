/* Plugin initializers */
$(document).ready(function() {
    $('.datetimepicker').each(function(_, datetimepicker) {
        var $datetimepicker = $(datetimepicker);
        var format = $datetimepicker.data('format') || 'DD.MM.YYYY';
        var view_mode = $datetimepicker.data('view-mode') || 'days';

        /* TODO: minDate and maxDate */
        $datetimepicker.datetimepicker({
            format: format,
            viewMode: view_mode,
        })
    })
});