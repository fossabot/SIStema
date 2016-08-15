import os

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont


class AbstractPreviewGenerator:
    template = '__template_not_found__'

    def __init__(self, attachment):
        self.attachment = attachment

    def generate(self, output_file):
        raise NotImplementedError


class ImagePreviewGenerator(AbstractPreviewGenerator):
    template = 'image.html'

    def generate(self, output_file):
        size = (64, 64)
        preview = Image.open(self.attachment.get_file_abspath())
        preview.thumbnail(size)
        preview.save(output_file, 'JPEG')


class TextPreviewGenerator(AbstractPreviewGenerator):
    template = 'text.html'

    def generate(self, output_file):
        text_file = open(self.attachment.get_file_abspath(), "r")
        size = (64, 96)
        image = Image.new('RGBA', size, (255, 255, 255))
        font_path = os.path.join(settings.BASE_DIR, 'web/modules/mail/static/mail/fonts/DroidSans.ttf')
        font = ImageFont.truetype(font_path, size=7)
        draw = ImageDraw.Draw(image)
        text = text_file.read(500)
        split_text = text.split('\n')
        for counter in range(min(12, len(split_text))):
            line = split_text[counter] + '\n'
            draw.text((7, 9 + counter * 7), line, fill=(100, 100, 100), font=font)
        image.save(output_file, 'JPEG')