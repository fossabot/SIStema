/*
 * Script for popup hint list in recipient-field
 */


$(document).ready
(
    function()
    {
        function split_by_commas(val)
        {
            return val.split(/,\s*/)
        }

        function extract_last(val)
        {
            return split_by_commas(val).pop()
        }

        $('#tags').autocomplete({
            source: function(request, response)
            {
                var search_value = extract_last(request.term);
                console.log(search_value)
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
            },
            focus: function()
            {
                return false;
            },
            select: function(event, ui)
            {
                var terms = split_by_commas(this.value);
                terms.pop();
                terms.push(ui.item.value);
                this.value = terms.join(', ');
                return false;
            }
        });
        $('.ui-helper-hidden-accessible').attr('style', 'display: none;')
    }
);