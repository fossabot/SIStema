from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.template.defaultfilters import filesizeformat
from django.utils.html import format_html
from django.forms.forms import BoundField


# TODO: move to the frontend application


class TextInputWithFaIcon(forms.TextInput):
    fa_type = None

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is not None:
            self.fa_type = attrs.pop('fa', self.fa_type)

    @property
    def fa_type_safe(self):
        return self.fa_type.replace(r'"', r'\"')

    def render(self, name, value, attrs=None):
        base_rendered = super().render(name, value, attrs=attrs)

        return '<label class="field prepend-icon">%s<label class="field-icon"><i class="fa fa-%s"></i></label>' % \
               (base_rendered, self.fa_type_safe)


class PasswordInputWithFaIcon(forms.PasswordInput, TextInputWithFaIcon):
    pass


class TextareaWithFaIcon(forms.Textarea):
    fa_type = None

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is not None:
            self.fa_type = attrs.pop('fa', self.fa_type)

    @property
    def fa_type_safe(self):
        return self.fa_type.replace(r'"', r'\"')

    def render(self, name, value, attrs=None):
        base_rendered = super().render(name, value, attrs=attrs)

        return '<label class="field prepend-icon">%s<label class="field-icon"><i class="fa fa-%s"></i></label>' % \
               (base_rendered, self.fa_type_safe)


class SistemaChoiceInput(widgets.ChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs

        block_or_online = 'inline' if 'inline' in attrs and attrs['inline'] else 'block'

        return format_html(
                '<label{} class="option option-alert {} mt5">{} <span class="{}"></span> {}</label>',
                label_for,
                block_or_online,
                self.tag(attrs),
                self.input_type,
                self.choice_label
        )


# TODO: it's not working and not used now
class ButtonGroup(widgets.NumberInput):
    def render(self, name, value, attrs=None):
        """
            <div class="btn-toolbar inline">
                <div class="btn-group inline" data-toggle="buttons-radio">
                    <a class="btn inline active" onClick="$('#theory_2').val('0')">0</a>
                    <a class="btn inline" onClick="$('#theory_2').val('1')">1</a>
                    <a class="btn inline" onClick="$('#theory_2').val('2')">2</a>
                    <a class="btn inline" onClick="$('#theory_2').val('3')">3</a>
                    <a class="btn inline" onClick="$('#theory_2').val('4')">4</a>
                    <a class="btn inline" onClick="$('#theory_2').val('5')">5</a>
                </div>
            </div>
        """
        hidden_input = widgets.HiddenInput().render(name, value, attrs)

        return format('''
        <div class="btn-toolbar inline">
            <div class="btn-group inline" data-toggle="buttons-radio">
                <a class="btn inline" onClick="$('#theory_2').val('4')">4</a>
                <a class="btn inline" onClick="$('#theory_2').val('5')">5</a>
            </div>
        </div>
        ''')


class SistemaRadioChoiceInput(SistemaChoiceInput, widgets.RadioChoiceInput):
    input_type = 'radio'


class SistemaCheckboxChoiceInput(SistemaChoiceInput, widgets.CheckboxChoiceInput):
    input_type = 'checkbox'


class SistemaRadioFieldRenderer(widgets.RadioFieldRenderer):
    choice_input_class = SistemaRadioChoiceInput
    outer_html = '{content}'
    inner_html = '{choice_value}'


class SistemaCheckboxFieldRenderer(widgets.CheckboxFieldRenderer):
    choice_input_class = SistemaCheckboxChoiceInput
    outer_html = '{content}'
    inner_html = '{choice_value}'


class SistemaRadioSelect(forms.RadioSelect):
    renderer = SistemaRadioFieldRenderer


class SistemaCheckboxSelect(forms.CheckboxSelectMultiple):
    renderer = SistemaCheckboxFieldRenderer


class RestrictedFileField(forms.FileField):
    """
    Same as FileField, but you can specify:
    * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    * max_upload_size - a number indicating the maximum file size allowed for upload (in bytes).
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_upload_size = kwargs.pop('max_upload_size', None)

        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        file = super().clean(data, initial)

        if self.content_types is not None:
            content_type = file.content_type
            if content_type not in self.content_types:
                raise ValidationError('Файл неверного формата')

        if self.max_upload_size is not None:
            file_size = file._size
            if file_size > self.max_upload_size:
                raise ValidationError('Размер файла (%s) превышет допустимый (%s)' % (
                    filesizeformat(file_size), filesizeformat(self.max_upload_size)))

        return data


def add_classes_to_label(f, classes=''):
    def func_wrapper(self, *args, **kwargs):
        # TODO: bug?
        if 'attrs' in kwargs:
            attrs = kwargs.pop('attrs', {})
            attrs['class'] = attrs.get('class', '') + ' ' + classes
            kwargs['attrs'] = attrs
        return f(self, *args, **kwargs)

    func_wrapper.__name__ = f.__name__
    func_wrapper.__module__ = f.__module__
    func_wrapper.__doc__ = f.__doc__
    return func_wrapper


BoundField.label_tag = add_classes_to_label(BoundField.label_tag, 'control-label')
widgets.Input.render = add_classes_to_label(widgets.Input.render, 'form-control')
widgets.Select.render = add_classes_to_label(widgets.Select.render, 'form-control')
