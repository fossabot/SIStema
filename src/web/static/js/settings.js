function saveEdit(index) {
    var form = $('#form-' + index);
    $.post(index, form.serialize());
    $('#setting-' + index).innerHTML = form.children[2].value;
}