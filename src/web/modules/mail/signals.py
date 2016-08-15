import bleach

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import EmailMessage


@receiver(pre_save, sender=EmailMessage)
def clean_html_text(instance, **kwargs):
    """Delete dangerous tags from email message text"""
    # Bleach is a whitelist-based HTML sanitizing library that escapes or strips markup and attributes.
    # Bleach is intended for sanitizing text from untrusted sources.
    # Whitelist could be found there:
    # https://github.com/mozilla/bleach/blob/master/bleach/__init__.py
    # There is a large discussion about sanitizing html in Python projects:
    # http://stackoverflow.com/questions/699468/python-html-sanitizer-scrubber-filter/812785
    # So in that discussion Bleach is most upvoted solution that passes tests.
    # Also, it's made by Mozilla and it's ready to production.
    # bleach.clean method deletes all dangerous tags and attributes,
    # but saves not dangerous like strong or i.
    if instance.html_text:
        cleaned_text = bleach.clean(instance.html_text)
        # Save '>' symbol for correct citing, it will have no affect on possible XSS attacks.
        cleaned_text = cleaned_text.replace('&gt;', '>')
        instance.html_text = cleaned_text
