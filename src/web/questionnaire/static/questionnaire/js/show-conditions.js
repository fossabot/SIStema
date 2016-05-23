$(document).ready(function(){
    function update_visibility($block, $options) {
        var checked_at_least_one = $options.filter(':visible:checked').length > 0;
        if (checked_at_least_one)
            $block.show(200);
        else {
            $block.hide(200, function () {
                $block.find('input[type=checkbox]').prop('checked', false);
                $block.find('input[type=radio]').prop('checked', false);
                $block.find('input[type=text]').val('');
                $block.find('textarea').val('');
            });
        }
    }

    $.fn.showOnlyIfOptionChecked = function ($options) {
        var $this = $(this);

        update_visibility($this, $options);
        $options.change(function() {
            update_visibility($this, $options);
        });
    }
});