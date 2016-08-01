from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

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



