import io
import re
import reportlab.platypus.doctemplate

from django.template import engines

from . import models


class GeneratorVisitor:
    first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
    all_cap_re = re.compile(r'([a-z0-9])([A-Z])')

    def _convert_camel_case_to_snake_case(self, name):
        s1 = self.first_cap_re.sub(r'\1_\2', name)
        return self.all_cap_re.sub(r'\1_\2', s1).lower()

    def visit(self, obj):
        class_name = obj.__class__.__name__
        method_name = 'visit_%s' % (self._convert_camel_case_to_snake_case(class_name), )
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                method(obj)


class DjangoTemplateGeneratorVisitor(GeneratorVisitor):
    def __init__(self, params, engine_name='django'):
        self.params = params
        self.engine = engines[engine_name]

    def visit_paragraph(self, paragraph):
        template = self.engine.from_string(paragraph.text)
        paragraph.text = template.render(self.params)


class TemplateGenerator:
    def __init__(self, document):
        self.document = document

    def generate(self, visitor=None):
        if isinstance(visitor, dict):
            visitor = DjangoTemplateGeneratorVisitor(visitor)

        models.Font.register_all_in_reportlab()
        models.FontFamily.register_all_in_reportlab()

        with io.BytesIO() as buffer:
            doc = reportlab.platypus.doctemplate.SimpleDocTemplate(
                buffer,
                rightMargin=self.document.right_margin,
                leftMargin=self.document.left_margin,
                topMargin=self.document.top_margin,
                bottomMargin=self.document.bottom_margin,
                pagesize=models.PageSize.get_pagesize(self.document.page_size)
            )

            blocks = self.document.blocks.order_by('order')
            build_blocks = [b.get_reportlab_block(visitor) for b in blocks]

            doc.build(build_blocks)

            return buffer.getvalue()
