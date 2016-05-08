# See https://www.djangosnippets.org/snippets/1926/ for details
# based on: http://www.djangosnippets.org/snippets/779/
from django.template import Library, Node, TemplateSyntaxError, Variable

register = Library()


class RangeNode(Node):
    def __init__(self, range_args, context_name):
        self.range_args = range_args
        self.context_name = context_name

    def render(self, context):
        range_args = [a.resolve(context) for a in self.range_args]
        context[self.context_name] = range(*range_args)
        return ""


@register.tag
def mkrange(parser, token):
    """
    Accepts the same arguments as the 'range' builtin and creates
    a list containing the result of 'range'.

    Syntax:
        {% mkrange [start,] stop[, step] as context_name %}

    For example:
        {% mkrange 5 10 2 as some_range %}
        {% for i in some_range %}
          {{ i }}: Something I want to repeat\n
        {% endfor %}

    Produces:
        5: Something I want to repeat
        7: Something I want to repeat
        9: Something I want to repeat
    """

    tokens = token.split_contents()
    fnctl = tokens.pop(0)

    def error():
        raise TemplateSyntaxError(
                "%s accepts the syntax: {%% %s [start,] stop[, step] as context_name %%}, where 'start', 'stop' and "
                "'step' must all be integers constants or variables." % (fnctl, fnctl))

    range_args = []
    while True:
        if len(tokens) < 2:
            error()

        token = tokens.pop(0)

        if token == 'as':
            break

        range_args.append(Variable(token))
        # range_args.append(int(token))

    if len(tokens) != 1:
        error()

    context_name = tokens.pop()

    return RangeNode(range_args, context_name)
