from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

from . import models


@login_required
def compose(request):
    return render(request, 'mail/compose.html')


@login_required
def contacts(request):
    NUMBER_OF_RETURNING_RECORDS = 10
    search_request = request.GET['search']
    try:
        email_user = models.SisEmailUser.objects.get(user=request.user)
    except models.EmailUser.DoesNotExist:
        return HttpResponseNotFound("Can't find your mail box.")
    records = models.ContactRecord.objects.filter(
        Q(owner=email_user) & (
            Q(person__sisemailuser__user__email__icontains=search_request) |
            Q(person__sisemailuser__user__first_name__icontains=search_request) |
            Q(person__sisemailuser__user__last_name__icontains=search_request) |
            Q(person__externalemailuser__display_name__icontains=search_request) |
            Q(person__externalemailuser__email__icontains=search_request)
        )
    )[:NUMBER_OF_RETURNING_RECORDS]
    filtered_records = []
    for rec in records:
        if isinstance(rec.person, models.ExternalEmailUser):
            filtered_records.append({'email': rec.person.email, 'display_name': rec.person.display_name})
        else:
            filtered_records.append({'email': rec.person.user.email,
                                     'display_name': rec.person.user.first_name + ' ' + rec.person.user.last_name})
    return JsonResponse({'records': filtered_records})


def can_user_view_message(user, email):
    if isinstance(email.sender, models.SisEmailUser) and user == email.sender.user:
        return True
    if email.recipients.filter(sisemailuser__user=user):
        return True
    if email.cc_recipients.filter(sisemailuser__user=user):
        return True
    return False


@login_required
def inbox(request):
    inbox_email_list = models.EmailMessage.objects.filter(
        Q(recipients__sisemailuser__user=request.user) |
        Q(cc_recipients__sisemailuser__user=request.user)
    ).order_by('-created_at')

    return render(request, 'mail/inbox.html', {
        'inbox_email_list': inbox_email_list,
    })


@login_required
def message(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)

    if not can_user_view_message(request.user, email):
        return HttpResponseForbidden()

    return render(request, 'mail/message.html', {
        'email': email,
    })
