from string import whitespace
import os

from django.contrib.auth.decorators import login_required
from django.core import urlresolvers, validators, exceptions
from django.db.models import Q, TextField
from django.db.models.expressions import Value
from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.html import strip_tags
from django import forms
from django.contrib import messages

from settings import api
from modules.mail.models import get_user_by_hash
from . import models, forms
from sistema.helpers import respond_as_attachment
from django.conf import settings
from sistema.uploads import save_file


# Parse recipients from string like: a@mail.ru, b@mail.ru, ...
def _get_recipients(string_with_recipients):
    recipients = []
    for recipient in string_with_recipients.split(', '):
        if recipient == '':
            continue
        try:
            validators.validate_email(recipient)
        except exceptions.ValidationError:
            # if recipient is not real email, skip it.
            continue
        query = models.EmailUser.objects.filter(
            Q(sisemailuser__user__email__iexact=recipient) |
            Q(externalemailuser__email__iexact=recipient)
        ).first()
        if query is not None:
            recipients.append(query)
        else:
            query = models.PersonalEmail.objects.annotate(
                full_email=Concat('email_name', Value('-'), 'hash', Value(settings.MAIL_DOMAIN),
                                  output_field=TextField())).filter(full_email__iexact=recipient).first()
            if query is not None:
                recipients.append(query.owner)
            else:
                external_user = models.ExternalEmailUser()
                external_user.email = recipient
                external_user.save()
                recipients.append(external_user)
    return recipients


# Save email to database(if email_id != None edit existing email)
def _save_email(request, email_form, email_id=None, email_status=models.EmailMessage.STATUS_DRAFT, uploaded_files=None):
    attachments = []
    if uploaded_files is not None:
        for file in uploaded_files:
            saved_attachment_filename = os.path.relpath(
                save_file(file, 'mail-attachments'),
                models.Attachment._meta.get_field('file').path
            )
            attachments.append(models.Attachment(
                original_file_name=file.name,
                file_size=file.size,
                content_type=file.content_type,
                file=saved_attachment_filename,
            ))

    email = models.EmailMessage()
    try:
        email.sender = models.SisEmailUser.objects.get(user=request.user)
    except models.EmailUser.DoesNotExist:
        return None
    email.status = email_status
    email.html_text = email_form['email_message']
    email.subject = email_form['email_subject']
    email.id = email_id
    email.created_at = timezone.now()

    # Nazarov Georgiy - Как я понял, в джанге инициализация связей ленивая и происходит только в момент сохранения
    with transaction.atomic():
        email.save()

    email.recipients.clear()
    email.cc_recipients.clear()
    for recipient in _get_recipients(email_form['recipients']):
        email.recipients.add(recipient)
    for cc_recipient in _get_recipients(email_form['cc_recipients']):
        email.cc_recipients.add(cc_recipient)
    with transaction.atomic():
        for attachment in attachments:
            attachment.save()
            email.attachments.add(attachment)
        email.save()
    return email


@login_required
def compose(request):
    """
        Initialization draft in database and redirecting to editor-page
    """
    try:
        email = models.EmailMessage.objects.get(sender=request.user.email_user.first(),
                                                status=models.EmailMessage.STATUS_RAW_DRAFT)
    except models.EmailMessage.DoesNotExist:
        # Empty message for current user not found. Let's create it.
        email = models.EmailMessage()
        try:
            email.sender = models.SisEmailUser.objects.get(user=request.user)
        except models.EmailUser.DoesNotExist:
            return HttpResponseNotFound('Can\'t find your email box.')

        email.status = models.EmailMessage.STATUS_RAW_DRAFT
        with transaction.atomic():
            email.save()

    url = urlresolvers.reverse('mail:edit', kwargs={'message_id': email.id})
    return redirect(url)


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


def sis_users(request):
    NUMBER_OF_RETURNING_RECORDS = 10
    search_request = request.GET['search']
    records = models.SisEmailUser.objects.filter(
        Q(user__first_name__icontains=search_request) | Q(user__last_name__icontains=search_request)
    )[:NUMBER_OF_RETURNING_RECORDS]
    filtered_records = [{'display_name': rec.display_name} for rec in records]
    return JsonResponse({'records': filtered_records})


def is_sender_of_email(user, email):
    return isinstance(email.sender, models.SisEmailUser) and user == email.sender.user


def is_recipient_of_email(user, email):
    return bool(email.recipients.filter(sisemailuser__user=user) or email.cc_recipients.filter(sisemailuser__user=user))


def can_user_view_message(user, email):
    return is_recipient_of_email(user, email) or is_sender_of_email(user, email)


def _is_message_dict_empty(email):
    """
    Returns True if email is empty
    :param email: dict-like object with email fields
    """
    FIELDS = ('recipients', 'email_subject', 'email_message')
    is_message_empty = True
    for field in FIELDS:
        if email[field]:
            is_message_empty = False
            break
    return is_message_empty


EMAILS_PER_PAGE = 20
PAGES_ON_PAGINATOR = 5  # Should be odd (i.e. 3, 5, 7 etc.)


def _get_max_page_num(mail_count):
    if mail_count == 0:
        return 1
    if mail_count % EMAILS_PER_PAGE == 0:
        return mail_count // EMAILS_PER_PAGE
    else:
        return mail_count // EMAILS_PER_PAGE + 1


def _get_start_and_end_page(page_index, max_page):
    if page_index <= PAGES_ON_PAGINATOR // 2:
        return 1, min(max_page, PAGES_ON_PAGINATOR)
    elif page_index > max_page - PAGES_ON_PAGINATOR // 2:
        return max(max_page - PAGES_ON_PAGINATOR + 1, 1), max_page
    else:
        return page_index - PAGES_ON_PAGINATOR // 2, page_index + PAGES_ON_PAGINATOR // 2


def _get_links_of_pages_to_show(view, page_index, mail_count):
    links = []
    start_page, end_page = _get_start_and_end_page(page_index, _get_max_page_num(mail_count))
    for i in range(start_page, end_page + 1):
        links.append(urlresolvers.reverse(view, kwargs={'page_index': i}))
    return links


def _get_standard_mail_list_params(mail_list, page_index, request):
    params = dict()
    params['mail_list'] = mail_list[(page_index - 1) * EMAILS_PER_PAGE: page_index * EMAILS_PER_PAGE]
    params['page'] = page_index
    params['show_previous'] = (page_index != 1)
    params['show_next'] = (page_index != _get_max_page_num(len(mail_list)))
    params['start_page'] = _get_start_and_end_page(page_index, _get_max_page_num(len(mail_list)))[0]
    params['user'] = request.user.email_user.first()
    return params


def _get_prev_link(view, page_index):
    if page_index != 1:
        return urlresolvers.reverse(view, kwargs={'page_index': page_index - 1})
    return ''


def _get_next_link(view, page_index, mail_count):
    if page_index < _get_max_page_num(mail_count):
        return urlresolvers.reverse(view, kwargs={'page_index': page_index + 1})
    return ''


def _read_page_index(page_index, mail_count):
    try:
        page_index = int(page_index)
        if page_index > _get_max_page_num(mail_count):
            return True, _get_max_page_num(mail_count)
        else:
            return False, page_index
    except ValueError:
        return True, 1


@login_required
def inbox(request, page_index='1'):
    mail_list = models.EmailMessage.get_not_removed().filter(status=models.EmailMessage.STATUS_ACCEPTED).filter(
        Q(recipients__sisemailuser__user=request.user) |
        Q(cc_recipients__sisemailuser__user=request.user)
    ).order_by('-created_at')

    do_redirect, page_index = _read_page_index(page_index, len(mail_list))
    if do_redirect:
        return redirect(urlresolvers.reverse('mail:inbox_page', kwargs={'page_index': page_index}))

    params = _get_standard_mail_list_params(mail_list, page_index, request)
    params['tab_links'] = _get_links_of_pages_to_show('mail:inbox_page', page_index, len(mail_list))
    params['prev_link'] = _get_prev_link('mail:inbox_page', page_index)
    params['next_link'] = _get_next_link('mail:inbox_page', page_index, len(mail_list))
    return render(request, 'mail/inbox.html', params)


@login_required
def sent(request, page_index='1'):
    mail_list = models.EmailMessage.get_not_removed().filter(status=models.EmailMessage.STATUS_SENT).filter(
        sender__sisemailuser__user=request.user,
    ).order_by('-created_at')

    do_redirect, page_index = _read_page_index(page_index, len(mail_list))
    if do_redirect:
        return redirect(urlresolvers.reverse('mail:sent_page', kwargs={'page_index': page_index}))

    params = _get_standard_mail_list_params(mail_list, page_index, request)
    params['tab_links'] = _get_links_of_pages_to_show('mail:sent_page', page_index, len(mail_list))
    params['prev_link'] = _get_prev_link('mail:sent_page', page_index)
    params['next_link'] = _get_next_link('mail:sent_page', page_index, len(mail_list))
    return render(request, 'mail/sent.html', params)


def drafts_list(request, page_index='1'):
    page_index = int(page_index)
    mail_list = models.EmailMessage.get_not_removed().filter(status=models.EmailMessage.STATUS_DRAFT).filter(
        sender__sisemailuser__user=request.user,
    ).order_by('-created_at')

    do_redirect, page_index = _read_page_index(page_index, len(mail_list))
    if do_redirect:
        return redirect(urlresolvers.reverse('mail:drafts_page', kwargs={'page_index': page_index}))

    params = _get_standard_mail_list_params(mail_list, page_index, request)
    params['tab_links'] = _get_links_of_pages_to_show('mail:drafts_page', page_index, len(mail_list))
    params['prev_link'] = _get_prev_link('mail:drafts_page', page_index)
    params['next_link'] = _get_next_link('mail:drafts_page', page_index, len(mail_list))
    return render(request, 'mail/drafts.html', params)


@login_required
def message(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)

    if not can_user_view_message(request.user, email):
        return HttpResponseForbidden()

    return render(request, 'mail/message.html', {
        'email': email,
        'allow_replying': is_recipient_of_email(request.user, email),
    })


MAX_STRING_LENGTH = 70


def get_citation_depth(string):
    """ Returns the citation depth of a sentence, i.e. 3 for ">>> Hello" and 2 for ">> Hello"  """
    current = 0
    while current < len(string) and string[current] == '>':
        current += 1
    return current


def ensure_beginning_whitespace(string):
    """ Adds a beginning whitespace if necessary """
    if string and string[0] != ' ':
        return ' %s' % string
    return string


def rstrip_if_not_space(line):
    if not line.isspace():
        return line.rstrip()
    return line


def cite_text(text):
    """ Returns cited(quoted) text. Follows RFC 3676. """
    lines = text.split('\n')
    cited_lines = []
    for line in lines:
        depth = get_citation_depth(line)  # Gets the depth of the current citation
        line = line[depth:]  # Deletes the old citation prefix
        new_string_prefix = '>' * (depth + 1)  # Creates the new citation prefix
        current_max_string_length = MAX_STRING_LENGTH - len(new_string_prefix)  # Max length for line without citation
        line = rstrip_if_not_space(line)  # Strips unnecessary whitespaces if line is not a space
        line = line.replace('\r', '')  # Removes all occurrences of '\r'
        while len(line) > current_max_string_length:
            search_position = current_max_string_length
            # Will try to find a whitespace where the line could be split
            while search_position >= 0 and line[search_position] not in whitespace:
                search_position -= 1
            if search_position != -1:  # If an appropriate place to insert a line-break was found
                result = line[:search_position]
                line = line[search_position + 1:]
            else:
                # Will try to find the first whitespace where the line could be split when a word is too long
                search_position = current_max_string_length + 1
                while search_position < len(line) and line[search_position] not in whitespace:
                    search_position += 1
                if search_position != len(line):  # If found
                    result = line[:search_position]
                    line = line[search_position + 1:]
                else:  # If an acceptable position was not found adds the whole line
                    result = line
                    line = ''
            # Add the resulting shortened line
            cited_lines.append('%s%s' % (new_string_prefix, ensure_beginning_whitespace(result)))
        # Add the remainder of the line (if it is not empty)
        if line:
            cited_lines.append('%s%s' % (new_string_prefix, ensure_beginning_whitespace(line)))

    return '\n'.join(cited_lines)


@login_required
def reply(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)

    if not can_user_view_message(request.user, email):
        return HttpResponseForbidden()

    email_subject = 'Re: %s' % email.subject

    recipients = list()
    recipients.append(email.sender.email)
    cc_recipients = list()

    for recipient in email.recipients.all():
        if isinstance(recipient, models.ExternalEmailUser) or recipient.user != request.user:
            recipients.append(recipient.email)

    for cc_recipient in email.cc_recipients.all():
        if isinstance(cc_recipient, models.ExternalEmailUser) or cc_recipient.user != request.user:
            cc_recipients.append(cc_recipient.email)
    print(cc_recipients[0])
    if email.sender.display_name.isspace():
        display_name = email.sender.email
    else:
        display_name = email.sender.display_name
    text = '\n \n%s:\n%s' % (display_name, cite_text(strip_tags(email.html_text)))

    form_data = {
        'email_subject': email_subject,
        'recipients': ', '.join(recipients),
        'cc_recipients': ', '.join(cc_recipients),
        'email_message': text,
    }

    uploaded_files = request.FILES.getlist('attachments')
    sending_email = _save_email(request, form_data,
                                email_status=models.EmailMessage.STATUS_DRAFT,
                                uploaded_files=uploaded_files)
    if sending_email is None:
        return HttpResponseNotFound('Can\'t find your email box.')
    else:
        return redirect(urlresolvers.reverse('mail:edit', kwargs={'message_id': sending_email.id}))


@login_required
def edit(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)

    if not is_sender_of_email(request.user, email):
        return HttpResponseForbidden()

    if email.status not in (models.EmailMessage.STATUS_DRAFT, models.EmailMessage.STATUS_RAW_DRAFT):
        # TODO: Make readable error message
        return HttpResponseForbidden()

    if request.method == 'GET':
        EMAILS_SEPARATOR = ', '

        recipients = EMAILS_SEPARATOR.join([recipient.email for recipient in email.recipients.all()])
        cc_recipients = EMAILS_SEPARATOR.join([cc_recipient.email for cc_recipient in email.cc_recipients.all()])

        form = forms.ComposeForm(initial={
            'recipients': recipients,
            'cc_recipients': cc_recipients,
            'email_subject': email.subject,
            'email_message': email.html_text,
        })
        return render(request, 'mail/compose.html', {
            'form': form,
            'message_id': message_id,
        })

    elif request.method == 'POST':
        form = forms.ComposeForm(request.POST)
        if form.is_valid():
            message_data = form.cleaned_data
            uploaded_files = request.FILES.getlist('attachments')
            email = _save_email(request, message_data, message_id, models.EmailMessage.STATUS_SENT, uploaded_files)
            if email is not None:
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect(urlresolvers.reverse('mail:sent'))
            else:
                # Error when sending
                # TODO: readable response
                pass
        else:
            messages.info(request, 'Не удалось отправить письмо.')
            return render(request, 'mail/compose.html', {
                'form': form,
                'message_id': message_id,
            })

    else:
        return HttpResponseBadRequest('Method is not supported')


@require_POST
def delete_email(request, message_id):
    email = get_object_or_404(models.EmailMessage, id=message_id)
    if not can_user_view_message(request.user, email):
        messages.info(request, 'Не удалось удалить письмо')
        return redirect(urlresolvers.reverse('mail:inbox'))
    email.is_remove = True
    email.save()
    messages.success(request, 'Письмо успешно удалено')
    return redirect(urlresolvers.reverse('mail:inbox'))


@login_required
@require_POST
def save_changes(request, message_id):
    """
    If email is not filled draft, do nothing.
    If email is filled draft, save it to database.
    """
    message_data = request.POST
    is_raw_draft = _is_message_dict_empty(message_data)

    SUCCESS_LABEL = 'is_successful'
    if is_raw_draft:
        return JsonResponse({SUCCESS_LABEL: True})

    email = _save_email(request, message_data, message_id, models.EmailMessage.STATUS_DRAFT)

    if email is None:
        return JsonResponse({SUCCESS_LABEL: False})
    return JsonResponse({SUCCESS_LABEL: True, 'id': email.id})


def can_user_download_attachment(user, attachment):
    return bool(attachment.emailmessage_set.filter(
        Q(attachments=attachment) &
        (Q(sender__sisemailuser__user=user) |
         Q(recipients__sisemailuser__user=user) |
         Q(cc_recipients__sisemailuser__user=user))
    ))


@login_required
def download_attachment(request, attachment_id):
    attachment = get_object_or_404(models.Attachment, id=attachment_id)
    if not can_user_download_attachment(request.user, attachment):
        return HttpResponseForbidden()
    return respond_as_attachment(
        request,
        attachment.get_file_abspath(),
        attachment.original_file_name
    )


def write(request):
    form = forms.WriteForm(initial={
        'email_subject': '',
        'recipients': '',
        'email_message': '',
        'text': ''
    })
    return render(request, 'mail/compose.html', {'form': form, 'no_draft': True})


def write_to(request, recipient_hash):
    recipient = get_user_by_hash(recipient_hash)
    if recipient is None:
        return HttpResponseNotFound()
    form = forms.WriteForm(initial={
        'email_subject': '',
        'recipients': recipient.display_name,
        'email_message': '',
        'text': ''
    })
    return render(request, 'mail/compose.html', {'form': form, 'no_draft': True})


@login_required
def preview(request, attachment_id):
    attachment = get_object_or_404(models.Attachment, id=attachment_id)
    if not can_user_download_attachment(request.user, attachment):
        return HttpResponseForbidden()
    return respond_as_attachment(
        request,
        attachment.get_preview_abspath(),
        attachment.original_file_name
    )


@require_POST
@login_required
def delete_all(request):
    id_list = []
    for field in request.POST:
        if 'email_id' in field:
            # get email id from string like 'email_id 13'
            email_id = field.split()[1]
            if can_user_view_message(request.user, models.EmailMessage.objects.get(id=email_id)):
                id_list.append(email_id)
            else:
                messages.info(request, 'Не удалось удалить письма.')
                return redirect(urlresolvers.reverse('mail:inbox'))
    models.EmailMessage.delete_emails_by_ids(id_list)
    messages.success(request, 'Письма успешно удалены.')
    return redirect(request.POST['next'])
