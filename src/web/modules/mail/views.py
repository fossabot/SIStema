from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
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
            Q(person__sisemailuser__user__email__icontains=search_request) |
            Q(person__sisemailuser__user__first_name__icontains=search_request) |
            Q(person__sisemailuser__user__last_name__icontains=search_request) |
            Q(person__externalemailuser__display_name__icontains=search_request) |
            Q(person__externalemailuser__email__icontains=search_request)
        )
    )
    filtered_records = []
    for rec in records:
        if isinstance(rec.person, models.ExternalEmailUser):
            filtered_records.append({'email': rec.person.email, 'display_name': rec.person.display_name})
        else:
            filtered_records.append({'email': rec.person.user.email,
                                     'display_name': rec.person.user.first_name + ' ' + rec.person.user.last_name})
    return JsonResponse({'records': filtered_records})
