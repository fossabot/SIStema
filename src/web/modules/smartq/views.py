# -*- coding: utf-8 -*-

import datetime
import types
import uuid

from django import forms
from django import shortcuts
from django.db import models
from django.http import response
import jinja2

heap_template = """
    <p>
        Постройте кучу минимумов из элементов:
        {% for x in heap_elements %}<b>{{ x }}</b>{% if not loop.last %}, {% endif %}{% endfor %}.
    </p>
    <div style="position: relative; width: 600px;">
        <canvas id="canvas-{{ uuid }}" width="800" height="400" style="width: 100%; border: 1px solid #ddd;"></canvas>
        <form action="" method="post">
            <div id="overlay-{{ uuid }}" style="width: 100%; position: absolute; top: 0; left: 0;">
            {% for k in form.fields %}
                {{ form.fields[k] }}
            {% endfor %}
            </div>
        </form>
    </div>
    <script>
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

            input = document.getElementById('{{ uuid }}-element_' + i);
            input.style['text-align'] = 'center';
            input.style.width = '4em';
            input.style.position = 'absolute';
            input.style.top = y * canvas_to_overlay - input.offsetHeight / 2 + 'px';
            input.style.left = x * canvas_to_overlay - input.offsetWidth / 2 + 'px';
        }

        ctx.stroke();
    }

    var canvas = document.getElementById('canvas-{{ uuid }}');
    var overlay = document.getElementById('overlay-{{ uuid }}');
    draw_heap(canvas, overlay, {{ heap_elements|length }});
    </script>
"""

# Geneartors in db:
# - Separate model for generators
# - Question uses generator with arguments (dictionary, list or both?)
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
        # TODO(artemtab): what kind of object to return?
        return {
            'answer_fields_count': len(elements),
            'heap_elements': elements,
        }


class Checker:
    def __init__(self):
        pass
"""

class SmartQForm(forms.Form):
    default_renderer = 'django.forms.renderers.Jinja2'

    def __init__(self, uuid, elements_count, *args, **kwargs):
        super().__init__(*args, auto_id=uuid + '-%s', **kwargs)

        self.elements_count = elements_count

        for i in range(elements_count):
            field_name = 'element_' + str(i + 1)
            self.fields[field_name] = forms.IntegerField().get_bound_field(self, field_name)


class Question(models.Model):
    short_name = models.CharField(max_length=100, unique=True)

    template = models.TextField()

    # TODO(Artem Tabolin): consider adding version control
    code = models.TextField()

    compiled_code = models.BinaryField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    modified_date = models.DateTimeField(auto_now=True)

    _implementation_cache = {}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seed = None
        self._generator = None

    # TODO: add global cache layer
    @property
    def _implementation(self):
        module = self._implementation_cache.get(self.short_name)
        if module is None or module.modified_date < self.modified_date:
            print("Module created")
            module = types.ModuleType(name=self.short_name)
            # TODO: add safety layer
            exec(self.code, module.__dict__)  # TODO: use compiled_code
            module.modified_date = self.modified_date

            self._implementation_cache[self.short_name] = module

        return module

    @property
    def generator(self):
        if self._generator is None:
            # TODO: what if seed is None here?
            self._generator = self._implementation.Generator(seed=self._seed)
        return self._generator

    def save(self, *args, **kwargs):
        # TODO: validate the code
        super().save(*args, **kwargs)

    def html(self):
        context = self.generator.generate()
        context['uuid'] = str(uuid.uuid4())
        context['form'] = SmartQForm(context['uuid'],
                                     context['answer_fields_count'])
        # TODO: add cache layer
        return jinja2.Template(self.template).render(context)

    def with_seed(self, seed):
        # TODO: consider something better
        self._seed = seed
        return self

def heap(request, seed="100500"):
    question = Question(
        short_name='build_heap',
        template=heap_template,
        code=heap_code,
        modified_date=datetime.datetime.now())

    return shortcuts.render(request, 'smartq/question.html', {
        'question': question.with_seed(seed)})
