import collections
import mimetypes
import os
import random
import string
import urllib.parse

from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, StreamingHttpResponse


def respond_as_zip(request, filename, zip_stream):
    response = StreamingHttpResponse(zip_stream, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; ' + filename_header(request, filename)
    return response


def respond_as_attachment(request, file_path, original_filename):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return HttpResponseNotFound()

    with open(file_path, 'rb') as fp:
        response = HttpResponse(fp.read())

    content_type, encoding = mimetypes.guess_type(original_filename)
    if content_type is None:
        content_type = 'application/octet-stream'
    response['Content-Type'] = content_type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    response['Content-Disposition'] = 'attachment; ' + filename_header(request, original_filename)
    return response


def filename_header(request, original_filename):
    filename_header = ''
    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename)
    return filename_header


# TODO: if extract_key_function is str, make extract_key_function from operator.attrgetter
def group_by(collection, extract_key_function, extract_value_function=None):
    if extract_value_function is None:
        def extract_value_function(x):
            return x

    result = collections.defaultdict(list)
    for item in collection:
        key = extract_key_function(item)
        value = extract_value_function(item)
        result[key].append(value)

    return result

def generate_random_name(length=10, alphabet=string.hexdigits):
    return ''.join(random.choice(alphabet) for _ in range(length))
