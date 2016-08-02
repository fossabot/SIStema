$(document).ready
(
    function()
    {
        $('#tags').autocomplete({source:
            function(request, response)
            {
                var search_value = request.term;
                var submit_url = $(document).find('.email-recipient').data('submit-url');
                var items = []

                $.get(submit_url + '?search=' + encodeURIComponent(search_value), function (data) {
                    var encoded_quote = encodeURIComponent('"')
                    for (var i = 0; i < data.records.length; i++) {
                        var label_data = '"' + data.records[i].display_name + '" <' + data.records[i].email + '>'
                        items.push({label: label_data,
                                    value: data.records[i].email});
                    }
                    response(items)
                },
                'json')
            }
        });
        $('.ui-helper-hidden-accessible').attr('style', 'display: none;')
    }
);