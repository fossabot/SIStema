from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from . import models


@login_required
def compose(request):
    pass


@login_required
def contacts(request):
    search_request = request.GET['search']
    user_id = request.user.pk
    email_user = models.SisEmailUser.objects.get(user=user_id)
    user_contact_list = models.ContactList.objects.get(owner=email_user.pk)
    records = models.ContactRecord.objects.filter(contact_list=user_contact_list.pk)
    filtered = {'users': []}
    for rec in records:
        if isinstance(rec.person, models.SisEmailUser):
            user_display_name = ' '.join((rec.person.user.first_name, rec.person.user.last_name,
                                          rec.person.user.email))
            owner_user_full_name = user_display_name
            if search_request in owner_user_full_name:
                filtered['users'].append({'display_name': user_display_name})
        else:
            user_display_name = ' '.join((rec.person.display_name, rec.person.email))
            if search_request in user_display_name:
                filtered['users'].append({'display_name': user_display_name})
    return JsonResponse(filtered)