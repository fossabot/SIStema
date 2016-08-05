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


MAX_STRING_LENGTH = 70


def get_citation_depth(string):
    # Returns the citation depth of a sentence, i.e. 3 for "> > > Hello" and 2 for "> > Hello"
    current = 0
    while current < len(string) and string[current] == '>':
        current += 1
    return current


def ensure_rfc_space_stuffing(line):
    if (line and line[0] == '>') or (len(line) >= 5 and line[:6] == 'From '):
        return ' %s' % line
    else:
        return line


def ensure_beginning_whitespace(string):  # Adds a beginning whitespace if necessary
    if string and string[0] != ' ':
        return ' %s' % string
    return string


def cite_text(text):
    lines = text.split("\n")
    cited_lines = []
    for line in lines:
        depth = get_citation_depth(line)  # Gets the depth of the current citation
        line = line[depth:]  # Deletes the old citation prefix
        new_string_prefix = ">" * (depth + 1)  # Creates the new citation prefix
        line = line.rstrip()  # Strips unnecessary whitespaces
        line = line.replace('\r', '')  # Removes all occurrences of '\r'
        line = ensure_rfc_space_stuffing(line)  # Ensures space-stuffing from RFC 3676 4.2 and 4.4
        while len(line) > MAX_STRING_LENGTH:
            current = MAX_STRING_LENGTH
            # Will try to find a whitespace where the line could be split
            while current >= 0 and line[current] not in whitespace:
                current -= 1
            if current != -1:  # If an appropriate place to insert a line-break was found
                result = line[:current]
                line = line[current + 1:]
            else:
                result = line
            # Add the resulting short line
            cited_lines.append('%s%s' % (new_string_prefix, ensure_beginning_whitespace(result)))
        # Add the remainder of the line
        cited_lines.append('%s%s' % (new_string_prefix, ensure_beginning_whitespace(line)))

    return '\n'.join(cited_lines)


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

    if email.sender.display_name.isspace():
        display = email.sender.email
    else:
        display = email.sender.display_name
    text = '\n\n%s:\n%s' % (display, cite_text(strip_tags(email.html_text)))

    form = forms.ComposeForm(initial={
        'email_theme': email_theme,
        'recipients': ", ".join(recipients),
        'email_message': text,
    })

    return render(request, 'mail/compose.html', {
        'form': form,
    })
