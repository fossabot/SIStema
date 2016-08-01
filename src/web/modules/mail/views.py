from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render

from . import models


@login_required
def compose(request):
    return render(request, 'mail/compose.html')


@login_required
def contacts(request):
    search_request = request.GET['search']
    user_id = request.user.id
    email_user = models.SisEmailUser.objects.get(user=user_id)
    user_contact_list = models.ContactList.objects.get(owner=email_user.id)
    records = models.ContactRecord.objects.filter(
        Q(contact_list=user_contact_list.id) & (
            Q(person__sisemailuser__user__email__contains=search_request) |
            Q(person__sisemailuser__user__first_name__contains=search_request) |
            Q(person__sisemailuser__user__last_name__contains=search_request) |
            Q(person__externalemailuser__display_name__contains=search_request) |
            Q(person__externalemailuser__email__contains=search_request)
        )
    )
    json = []
    for rec in records:
        if isinstance(rec.person, models.ExternalEmailUser):
            json.append({'email': rec.person.email, 'display_name': rec.person.display_name})
        else:
            json.append({'email': rec.person.user.email,
                         'display_name': rec.person.user.first_name + ' ' + rec.person.user.last_name})
    return HttpResponse({'records': json}) 
