from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from . import documents
from . import models


@login_required
def download(request, document_type):
    document_type = get_object_or_404(models.DocumentType, school=request.school, short_name=document_type)
    document_generator = documents.DocumentGenerator(request.school)
    document = document_generator.generate(document_type, request.user)

    response = HttpResponse(content_type='application/pdf')
    filename = '%s. %s' % (request.school.full_name, document_type.name)
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (filename, )
    response['Content-Type'] = 'application/pdf'
    response.write(document)

    return response
