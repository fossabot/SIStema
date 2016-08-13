from collections import OrderedDict

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
                                     'class': 'form-control mb10 do_hints',
                                     'rows': '10',
                                     'placeholder': 'Начните вводить почту',
                                     'data-submit-url': urlresolvers.reverse_lazy('mail:contacts')
                                 }
                                 ))
    cc_recipients = forms.CharField(max_length=MAXIMUM_LENGTH_OF_RECIPIENTS,
                                    required=False,
                                    label='',
                                    label_suffix='',
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control mb10 do_hints',
                                        'rows': '10',
                                        'placeholder': 'Копия: Начните вводить почту',
                                        'data-submit-url': urlresolvers.reverse_lazy('mail:contacts'),
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


class WriteForm(ComposeForm):
    MAXIMUM_AUTHOR_LENGTH = 5000
    ORDER = (
        'author_name', 'author_email', 'recipients', 'email_subject', 'email_message', 'attachments'
    )

    def __init__(self, *args, **kwargs):
        super(WriteForm, self).__init__(*args, **kwargs)
        fields = OrderedDict()
        for key in self.ORDER:
            fields[key] = self.fields.pop(key)
        self.fields = fields

    author_email = forms.CharField(max_length=MAXIMUM_AUTHOR_LENGTH,
                                    required=True,
                                    label='',
                                    label_suffix='',
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control mb10',
                                        'rows': '10',
                                        'placeholder': 'Введите свой e-mail адрес',
                                    }))
    author_name = forms.CharField(max_length=MAXIMUM_AUTHOR_LENGTH,
                                  required=True,
                                  label='',
                                  label_suffix='',
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control mb10',
                                      'rows': '10',
                                      'placeholder': 'Введите свое имя',
                                  }))
    recipients = forms.CharField(max_length=ComposeForm.MAXIMUM_LENGTH_OF_RECIPIENTS,
                                 required=True,
                                 label='',
                                 label_suffix='',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control mb10 do_hints',
                                     'rows': '10',
                                     'placeholder': 'Начните вводить имя',
                                     'data-submit-url': urlresolvers.reverse_lazy('mail:sis_users')
                                 }
                                 ))


class ContactEditorForm(forms.Form):
    MAXIMUM_NAME_LENGTH = 5000

    display_name = forms.CharField(max_length=MAXIMUM_NAME_LENGTH,
                                   label='Имя',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control mb10',
                                       'placeholder': 'Введите имя',
                                   }),
                                    )

    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control mb10',
                                 'placeholder': 'Введите email',
                             }))
