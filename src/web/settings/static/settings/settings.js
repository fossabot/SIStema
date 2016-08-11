function saveEdit(index) {
    var form = $('#form-' + index);
    $.post(index, form.serialize());
    $('#setting-' + index).html(form.children[2].value);
}