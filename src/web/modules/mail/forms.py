from django import forms


class ComposeForm(forms.Form):
    MAXIMUM_LETTER_IN_LETTERS = 5000
    MAXIMUM_THEME_LENGTH = 1000
    recipients = forms.CharField(max_length=MAXIMUM_LETTER_IN_LETTERS,
                                 required=True,
                                 label='',
                                 label_suffix='',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control mb10',
                                     'id': 'email-text',
                                     'rows': '10',
                                     'maxlength': MAXIMUM_LETTER_IN_LETTERS,
                                     'placeholder': 'Начните вводить почту',
                                 }))
    email_theme = forms.CharField(max_length=MAXIMUM_THEME_LENGTH,
                                  required=False,
                                  label='',
                                  label_suffix='',
                                  widget=forms.TextInput(attrs={
                                     'class': 'form-control mb10',
                                     'id': 'email-theme',
                                     'placeholder': 'Тема',
                                     'maxlength': MAXIMUM_THEME_LENGTH,
                                 }))
    email_message = forms.CharField(max_length=MAXIMUM_LETTER_IN_LETTERS,
                                    required=False,
                                    label='',
                                    label_suffix='',
                                    widget=forms.Textarea(attrs={
                                        'class': 'form-control mb10',
                                        'id': 'email-text',
                                        'placeholder': 'Текст письма',
                                        'maxlength': MAXIMUM_LETTER_IN_LETTERS,
                                    }))
