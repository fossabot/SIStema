from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags

from . import models, forms

from string import whitespace


@login_required
def compose(request):
    form = forms.ComposeForm()
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
    filtered_records = []
    for rec in records:
        if isinstance(rec.person, models.ExternalEmailUser):
            filtered_records.append({'email': rec.person.email, 'display_name': rec.person.display_name})
        else:
            filtered_records.append({'email': rec.person.user.email,
                                     'display_name': rec.person.user.first_name + ' ' + rec.person.user.last_name})
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


def get_depth(string):
    current = 0
    while string[current] == '>':
        current += 1
    return current


def cite_text(text):
    MAX_STRING_LENGTH = 70
    text = strip_tags(text)
    lines = text.split("\n")
    final = list()
    for line in lines:
        depth = get_depth(line)
        new_depth_string = '>' * (depth + 1)
        line = line[depth:]
        while len(line) > MAX_STRING_LENGTH:
            current = MAX_STRING_LENGTH
            while current >= 0 and line[current] not in whitespace:
                current -= 1
            if current == -1:
                result = line[:MAX_STRING_LENGTH]
                line = line[MAX_STRING_LENGTH:]
            else:
                result = line[:current]
                line = line[current + 1:]
            final.append('%s %s' % (new_depth_string, result))
        final.append('%s %s' % (new_depth_string, line))
    return '\n'.join(final)


@login_required
def reply(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)

    if not can_user_view_message(request.user, email):
        return HttpResponseForbidden()

    email_theme = 'Re: %s' % email.subject

    recipients = list()
    recipients.append(email.sender.email)

    for recipient in email.recipients.all():
        if isinstance(recipient, models.ExternalEmailUser) or recipient.user != request.user:
            recipients.append(recipient.email)

    for cc_recipient in email.cc_recipients.all():
        if isinstance(cc_recipient, models.ExternalEmailUser) or cc_recipient.user != request.user:
            recipients.append(cc_recipient.email)

    form = forms.ComposeForm(initial={
        'email_theme': email_theme,
        'recipients': ", ".join(recipients),
        'email_message': cite_text(email.html_text)
    })

    return render(request, 'mail/compose.html', {
        'form': form,
    })
