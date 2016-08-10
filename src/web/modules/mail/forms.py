from django import forms
from django.core import urlresolvers


class ComposeForm(forms.Form):
    MAXIMUM_NUMBER_LETTERS_IN_EMAIL = 5000
    MAXIMUM_SUBJECT_LENGTH = 1000
    MAXIMUM_LENGTH_OF_RECIPIENTS = 1000
    recipients = forms.CharField(max_length=MAXIMUM_LENGTH_OF_RECIPIENTS,
                                 required=True,
                                 label='',
                                 label_suffix='',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control mb10',
                                     'rows': '10',
                                     'placeholder': 'Начните вводить почту',
                                     'data-submit-url': urlresolvers.reverse_lazy('mail:contacts')
                                    }
                                 ))
    email_subject = forms.CharField(max_length=MAXIMUM_SUBJECT_LENGTH,
                                    required=False,
                                    label='',
                                    label_suffix='',
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control mb10',
                                        'placeholder': 'Тема',
                                    }))
    email_message = forms.CharField(max_length=MAXIMUM_NUMBER_LETTERS_IN_EMAIL,
                                    required=False,
                                    label='',
                                    label_suffix='',
                                    strip=False,
                                    widget=forms.Textarea(attrs={
                                        'class': 'form-control mb10',
                                        'placeholder': 'Текст письма',
                                    }))
    attachments = forms.FileField(required=False,
                                 label='',
                                 label_suffix='',
                                 widget=forms.ClearableFileInput(attrs={
                                     'multiple': True,
                                 })
                                 )