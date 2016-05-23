$(document).ready(function(){
    function update_visibility($block, $options) {
        var checked_at_least_one = $options.filter(':visible:checked').length > 0;
        if (checked_at_least_one)
            $block.show(200);
        else {
            $block.hide(200, function () {
                $block.find('input[type=checkbox]').prop('checked', false).change();
                $block.find('input[type=radio]').prop('checked', false).change();
                $block.find('input[type=text]').val('');
                $block.find('textarea').val('');
            });
        }
    }

    $.fn.showOnlyIfOptionChecked = function ($options) {
        var $this = $(this);

        update_visibility($this, $options);

        /* We need to watch for all elements with the same name
         * because there are radio buttons which hire `change` only for new selected items
         */
        var $watched_inputs = $options;
        $options.each(function (i, el) {
            $watched_inputs = $watched_inputs.add($('input[name=' + $(el).attr('name') + ']'));
        });
        $watched_inputs.change(function() {
            update_visibility($this, $options);
        });
    }
});