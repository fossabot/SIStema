from django import template
import markdown

# Markdown filter for templates
# See http://www.jw.pe/blog/post/using-markdown-django-17/ for details

register = template.Library()


@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    markdown.markdown()
    return markdown.markdown(text, safe_mode='escape')