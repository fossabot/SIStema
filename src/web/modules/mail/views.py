from django.contrib.auth.decorators import login_required
from django.db.models import Q, TextField
from django.db.models.expressions import Value
from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone

from . import models, forms


# Parse recipients from string like: a@mail.ru, b@mail.ru, ...
def _get_recipients(string_with_recipients):
    recipients = []
    for recipient in string_with_recipients.split(', '):
        if models.EmailUser.objects.filter(
                        Q(sisemailuser__user__email__iexact=recipient) |
                        Q(externalemailuser__email__iexact=recipient)
        ).exists():
            recipients.append(models.EmailUser.objects.get(
                Q(sisemailuser__user__email__iexact=recipient) |
                Q(externalemailuser__email__iexact=recipient)
            ))
        else:
            if models.PersonalEmail.objects.annotate(
                    full_email=Concat('email_name', Value('-'), 'hash', Value('@sistema.lksh.ru'),
                                      output_field=TextField())).filter(full_email__iexact=recipient).exists():
                recipients.append(models.PersonalEmail.objects.annotate(
                    full_email=Concat('email_name', Value('-'), 'hash', Value('@sistema.lksh.ru'),
                                      output_field=TextField())).get(full_email__iexact=recipient).owner)
            else:
                external_user = models.ExternalEmailUser()
                external_user.email = recipient
                external_user.save()
                recipients.append(external_user)
    return recipients


# Save email to database(if email_id != None edit exist email)
def _save_email(request, email_form, email_id=None):
    email = models.EmailMessage()
    try:
        email.sender = models.SisEmailUser.objects.get(user=request.user)
    except models.EmailUser.DoesNotExist:
        return None
    email.status = models.EmailMessage.STATUS_DRAFT
    email.html_text = email_form['email_message']
    email.subject = email_form['email_subject']
    email.id = email_id
    email.created_at = timezone.now()
    with transaction.atomic():
        email.save()
        for recipient in _get_recipients(email_form['recipients']):
            email.recipients.add(recipient)
        email.save()
    return email


@login_required
def compose(request):
    if request.method == 'POST':
        form = forms.ComposeForm(request.POST)
    else:
        form = forms.ComposeForm()
    if form.is_valid():
        _save_email(request, form.cleaned_data)
        # TODO: make feedback
    else:
        pass
    return render(request, 'mail/compose.html', {'form': form})


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
    filtered_records = [{'email': rec.person.email, 'display_name': rec.person.display_name}
                        for rec in records]
    return JsonResponse({'records': filtered_records})


def is_sender_of_email(user, email):
    return isinstance(email.sender, models.SisEmailUser) and user == email.sender.user


def can_user_view_message(user, email):
    if is_sender_of_email(user, email):
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


@login_required
def send_email(request):
    if request.method == 'POST':
        form = forms.ComposeForm(request.POST)
        if form.is_valid():
            return JsonResponse({'result': 'ok'})
        else:
            return JsonResponse({'result': 'fail'})
    return JsonResponse({'error': 'bad method'})


@login_required
def reply(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)

    if not can_user_view_message(request.user, email):
        return HttpResponseForbidden()

    return render(request, 'mail/message.html', {
        'email': email,
    })


@login_required
def edit(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)

    if not is_sender_of_email(request.user, email):
        return HttpResponseForbidden()

    if email.status != models.EmailMessage.STATUS_DRAFT:
        # TODO: Make readable error message
        return HttpResponseForbidden()

    EMAILS_SEPARATOR = ', '

    recipients = EMAILS_SEPARATOR.join([recipient.email for recipient in email.recipients.all()])

    form = forms.ComposeForm(data={
        'recipients': recipients,
        'email_theme': email.subject,
        'email_message': email.html_text,
    })

    return render(request, 'mail/compose.html', {
        'form': form,
    })


@require_POST
def delete_email(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)
    if not can_user_view_message(request.user, email):
        return HttpResponseForbidden()
    email.delete()
    return redirect('/mail')


@login_required
def save_changes(request, message_id):
    message_data = request.POST
    email = _save_email(request, message_data, message_id)

    SUCCESS_LABEL = 'is_successful'

    if email is None:
        return JsonResponse({SUCCESS_LABEL: False})
    return JsonResponse({SUCCESS_LABEL: True, 'id': email.id})
