# -*- coding: utf-8 -*-

import datetime
import json
import types
import uuid

from django import forms
from django import shortcuts
from django.db import models
from django.http import response
import jinja2

from modules.smartq import api

heap_template_html = """
    <p>
        Постройте кучу минимумов из элементов:
        {% for x in data.heap_elements %}<b>{{ x }}</b>{% if not loop.last %}, {% endif %}{% endfor %}.
    </p>
    <div style="position: relative; width: 600px;">
        <canvas id="canvas-{{ short_name }}" width="800" height="400" style="width: 100%; border: 1px solid #ddd;"></canvas>
        <form action="" method="post">
            <div id="overlay-{{ short_name }}" style="width: 100%; position: absolute; top: 0; left: 0;">
            {% for k in form.fields %}
                {{ form.fields[k] }}
            {% endfor %}
            </div>
        </form>
    </div>
"""

heap_template_js = """
(function() {
    function draw_heap(canvas, overlay, n) {
        var depth = Math.floor(1 + Math.log2(n));
        var ctx = canvas.getContext('2d');
        var canvas_width = canvas.width;
        var canvas_height = canvas.height;
        var overlay_width = canvas.offsetWidth;
        var overlay_height = canvas.offsetHeight;
        var canvas_to_overlay = overlay_width / canvas_width;

        var levels = [];
        for (var i = 0; i <= depth; ++i) {
            levels.push(i * canvas_height / (depth + 1));
        }

        var nodes = {};
        var level = 0, level_size = 0, j = 0;
        for (var i = 1; i <= n; ++i, ++j) {
            if (!(i & (i - 1))) {
                level_size = 1 << level;
                level++;
                j = 0;
                var node_width = canvas_width / level_size;
            }

            var x = node_width * (0.5 + j);
            var y = levels[level];
            nodes[i] = {x: x, y: y};

            if (i > 1) {
                var parent_node = nodes[Math.floor(i / 2)];
                ctx.moveTo(parent_node.x, parent_node.y);
                ctx.lineTo(x, y);
            }

            input = document.getElementById('{{ short_name }}-element_' + i);
            input.style['text-align'] = 'center';
            input.style.width = '4em';
            input.style.position = 'absolute';
            input.style.top = y * canvas_to_overlay - input.offsetHeight / 2 + 'px';
            input.style.left = x * canvas_to_overlay - input.offsetWidth / 2 + 'px';
        }

        ctx.stroke();
    }

    var canvas = document.getElementById('canvas-{{ short_name }}');
    var overlay = document.getElementById('overlay-{{ short_name }}');
    draw_heap(canvas, overlay, {{ data.heap_elements|length }});
})();
"""

heap_code = """
import random

class Generator:
    # TODO(artemtab): where to put seed?
    def __init__(self, seed):
        self.seed = seed
        self.size = 10

    def generate(self):
        # TODO(artemtab): how it behaves when there are several threads?
        # TODO(artemtab): most probably we need strong consistency 
        state = random.getstate()
        random.seed(self.seed)

        elements = random.sample(range(100), self.size)

        random.setstate(state)
        return api.GeneratedQuestionData(answer_fields=[0] * len(elements),
                                         heap_elements=elements)


class Checker:
    def __init__(self):
        pass
"""

class SmartQForm(forms.Form):
    default_renderer = 'django.forms.renderers.Jinja2'

    def __init__(self, prefix, field_specs, *args, **kwargs):
        super().__init__(*args, auto_id=prefix + '-%s', **kwargs)

        self.field_specs = field_specs

        for i in range(len(field_specs)):
            # TODO: add prefix to name
            field_name = 'element_' + str(i + 1)
            self.fields[field_name] = forms.IntegerField().get_bound_field(self, field_name)


class Question(models.Model):
    short_name = models.CharField(max_length=100, unique=True)

    template_html = models.TextField()

    template_css = models.TextField(blank=True, default='')

    template_js = models.TextField(blank=True, default='')

    # TODO(Artem Tabolin): consider adding version control
    code = models.TextField()

    compiled_code = models.BinaryField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    modified_date = models.DateTimeField(auto_now=True)

    _implementation_cache = {}
    _template_cache = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seed = None
        self._generator = None

    @property
    def _implementation(self):
        module = self._implementation_cache.get(self.short_name)
        if module is None or module.modified_date < self.modified_date:
            module = types.ModuleType(name=self.short_name)
            module.api = api
            # TODO: add safety layer
            exec(self.code, module.__dict__)  # TODO: use compiled_code
            module.modified_date = self.modified_date

            self._implementation_cache[self.short_name] = module

        return module

    def save(self, *args, **kwargs):
        # TODO: validate the code
        super().save(*args, **kwargs)

    def generate_with_seed(self, seed):
        data = self._implementation.Generator(seed=seed).generate()
        # TODO: replace with objects.create
        return GeneratedQuestion(
            base_question=self,
            seed=seed,
            data_json=json.dumps(data.__dict__))


class GeneratedQuestion(models.Model):
    base_question = models.ForeignKey(Question)

    seed = models.CharField(max_length=100)

    data_json = models.CharField()

    # TODO: what about custom manager which is doing serialization itself?

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None

    @property
    def data(self):
        if self._data is None:
            data_dict = json.loads(self.data_json)
            self._data = api.GeneratedQuestionData(**data_dict)
        return self._data

    def html(self):
        context = {
            'short_name': self.base_question.short_name,
            'data': self.data,
            'form': SmartQForm(self.base_question.short_name,
                               self.data.answer_fields)
        }

        # TODO: add cache layer
        return jinja2.Template(self.base_question.template_html).render(context)

    def css(self):
        context = {
            'short_name': self.base_question.short_name,
            'data': self.data,
        }

        # TODO: add cache layer
        return jinja2.Template(self.base_question.template_css).render(context)

    def js(self):
        context = {
            'short_name': self.base_question.short_name,
            'data': self.data,
        }

        # TODO: add cache layer
        return jinja2.Template(self.base_question.template_js).render(context)


def heap(request, seed="100500"):
    question = Question(
        short_name='build_heap',
        template_html=heap_template_html,
        template_js=heap_template_js,
        code=heap_code,
        modified_date=datetime.datetime.now())

    return shortcuts.render(request, 'smartq/question.html', {
        'question': question.generate_with_seed(seed)})
