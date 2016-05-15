from django import forms

import sistema.forms


class EnrolledScanForm(forms.Form):
    scan = sistema.forms.RestrictedFileField(max_upload_size=2 * 1024 * 1024,
                                             required=True,
                                             label='',
                                             label_suffix='')
