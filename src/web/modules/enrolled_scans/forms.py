from django import forms

import frontend.forms


class EnrolledScanForm(forms.Form):
    scan = frontend.forms.RestrictedFileField(max_upload_size=2 * 1024 * 1024,
                                              required=True,
                                              label='',
                                              label_suffix='')
