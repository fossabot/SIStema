$($('.clear')[0]).hide();

function saveEdit(index) {
    var form = $('#form-' + index);
    $.post(index + '/', form.serialize());
    $('#setting-' + index).html(form.children[2].value);
}

function search() {
    var query = $('#search-query').val().toLowerCase();
    if (!query) {
        return
    }
    $('.settings-item').each(function (num, value) {
        var elem = $(this);
        var header = $($($(elem[0].firstChild)[0].nextElementSibling)[0]);
        var description = $($('.description', elem)[0]);

        if (!(header.text().toLowerCase().search(query) != -1 ||
            description.text().toLowerCase().search(query) != -1)) {
            elem.hide();
        }
    })

    $($('.clear')[0]).show();
}

function clearSearch() {
    $('#search-query').val('');
    $('.settings-item').each(function (num, value) {
        var elem = $(this);
        elem.show();
    });

    $($('.clear')[0]).hide();
}