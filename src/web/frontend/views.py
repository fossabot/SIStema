from django.http.response import JsonResponse, HttpResponseNotFound
import sistema.staff
import importlib
from . import table


# TODO: check access more accurate
@sistema.staff.only_staff
def table_data(request, table_name):
    get = dict(request.GET)
    filter = get.pop('filter', [''])
    identifiers = get

    table_module_name, table_class_name = table_name.rsplit('.', 1)
    try:
        table_module = importlib.import_module(table_module_name)
        table_class = getattr(table_module, table_class_name)
        if not issubclass(table_class, table.Table):
            raise AttributeError()
    except (ImportError, AttributeError):
        return HttpResponseNotFound('Bad table name')

    try:
        restored_table = table_class.restore(identifiers)
    except Exception:
        return HttpResponseNotFound('Invalid parameters for table')

    restored_table.apply_filter(filter[0])

    return JsonResponse({
        'table_name': table_name,
        'rows': list(restored_table.rows()),
        'filter': filter,
        'identifiers': identifiers,
    })
