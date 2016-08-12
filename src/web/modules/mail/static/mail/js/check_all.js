function get_checked(checkbox_group) {
    var checked = [];
    var checkboxes = $('input:checkbox[checkbox_group="' + checkbox_group + '"]');
    for (var i = 1; i < checkboxes.length; ++i) {
        if ($('#' + checkboxes[i].getAttribute('id')).prop('checked')) {
            checked.push(checkboxes[i].getAttribute('id'));
        }
    }
    return checked
}

function change_checked(checkbox_group, val) {
    val = !!val;
    $('input:checkbox[checkbox_group="' + checkbox_group + '"]').prop('checked', val);
}
