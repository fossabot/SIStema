/*
 * Script for popup hint list in recipient-field
 */


$(document).ready
(
    function () {
        function split_by_commas(val) {
            return val.split(/,\s*/)
        }

        function extract_last(val) {
            return split_by_commas(val).pop()
        }

        $('#id_recipients').autocomplete({
            source: function (request, response) {
                var search_value = extract_last(request.term);
                var submit_url = $('#id_recipients').attr('data-submit-url');
                var items = [];

                $.get(submit_url + '?search=' + encodeURIComponent(search_value), function (data) {
                        for (var i = 0; i < data.records.length; i++) {
                            var label_data = data.records[i].display_name;
                            if (data.records[i].email != undefined) {
                                label_data = '"' + label_data + '" <' + data.records[i].email + '>';
                                items.push({
                                    label: label_data,
                                    value: data.records[i].email
                                });
                            } else {
                                items.push({
                                    label: label_data,
                                    value: label_data
                                });
                            }

                        }
                        response(items)
                    },
                    'json')
            },
            focus: function () {
                return false;
            },
            select: function (event, ui) {
                var terms = split_by_commas(this.value);
                terms.pop();
                terms.push(ui.item.value);
                this.value = terms.join(', ');
                terms.push("");
                return false;
            },
            minLength: 1
        });
        $('.ui-helper-hidden-accessible').attr('style', 'display: none;')
    }
);