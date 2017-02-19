import random
import uuid

from django import shortcuts
from django.http import response
import jinja2

# Geneartors in db:
# - Separate model for generators
# - Question uses generator with arguments (dictionary, list or both?)
class HeapGenerator:
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
            'heap_elements': elements,
        }


class HeapRenderer:
    def __init__(self):
        template_str = """
            <p>
                Постройте кучу минимумов из элементов:
                {% for x in heap_elements %}<b>{{ x }}</b>{% if not loop.last %}, {% endif %}{% endfor %}.
            </p>
            <div style="position: relative; width: 600px;">
                <canvas id="canvas-{{ uuid }}" width="800" height="400" style="width: 100%; border: 1px solid #ddd;"></canvas>
                <form action="" method="post">
                    <div id="overlay-{{ uuid }}" style="width: 100%; position: absolute; top: 0; left: 0;"></div>
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

                    input = document.createElement('input');
                    overlay.appendChild(input);
                    input.type = 'text';
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
        self.template = jinja2.Template(template_str)

    def render(self, args):
        context = dict(args)
        context['uuid'] = uuid.uuid4()
        return self.template.render(context)


class Checker:
    def __init__(self):
        pass


class Question:
    generator_cls = HeapGenerator
    renderer_cls = HeapRenderer
    checker_cls = Checker

    def __init__(self, seed):
        # TODO: It should use seed + args from model
        self.generator = self.generator_cls(seed)
        self.renderer = self.renderer_cls()
        self.checker = self.checker_cls()

    def html(self):
        return self.renderer.render(self.generator.generate())


def heap(request, seed="100500"):
    question = Question(seed)
    return shortcuts.render(request, 'smartq/question.html', {
        'question': question})
