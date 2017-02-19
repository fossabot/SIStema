import random

from django.http import response
import jinja2

# Geneartors in db:
# - Separate model for generators
# - Question uses generator with arguments (dictionary, list or both?)
class HeapGenerator:
    # TODO(artemtab): where to put seed?
    def __init__(self, seed):
        self.seed = seed
        self.size = 13

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
            Hi! The heap elements are <b>{{ heap_elements }}</b>
        """
        self.template = jinja2.Template(template_str)

    def render(self, args):
        return self.template.render(args)


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
    return response.HttpResponse(question.html())
