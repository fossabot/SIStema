from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from . import models


@login_required
def inbox(request):
    ordered_inbox_email_list = models.EmailMessage.objects.filter(
        Q(recipients__sisemailuser__user=request.user) |
        Q(cc_recipients__sisemailuser__user=request.user)
    ).order_by('-created_at')

    return render(request, 'mail/inbox.html', {
        'ordered_inbox_email_list': ordered_inbox_email_list,
    })


@login_required
def message(request, message_id):
    #email = models.EmailMessage.objects.get_(id=message_id)
    email = get_object_or_404(models.EmailMessage, id=message_id)

    return render(request, 'mail/message.html', {
        'message_id': message_id,
        'email': email,
    })


