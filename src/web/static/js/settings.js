function saveEdit(index) {
    $.post(index, $('#form-' + index).serialize());
    document.getElementById("setting-" + index).innerHTML = document.getElementById("form-" + index).children[2].value;
}