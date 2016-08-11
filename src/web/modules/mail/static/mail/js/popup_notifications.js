$(document).ready(
    function () {
        function get_request_params() {
            var request = location.search;
            var tmp = (request.substr(1)).split('&');
            var parameters = {};
            for (var i = 0; i < tmp.length; ++i) {
                var param = tmp[i].split('=');
                parameters[param[0]] = param[1];
            }
            return parameters
        }

        var params = get_request_params();
        var text;
        var type;
        if (params.type == 'delete') {
            switch (params.result) {
                case 'ok':
                    text = 'Письмо успешно удалено.';
                    type = 'success';
                    break;
                case 'fail':
                    text = 'Не удалось удалить письмо.';
                    type = 'info';
                    break;
            }
        }

        if (params.type == 'send') {
            switch (params.result) {
                case 'ok':
                    text = 'Письмо успешно отправлено.';
                    type = 'success';
                    break;
                case 'fail':
                    text = 'Не удалось отправить письмо.';
                    type = 'info';
                    break;
            }

        }
        if (text && type)
            new PNotify({
                title: 'Уведомление',
                text: text,
                type: type,
                hide: false
            });
    }
);