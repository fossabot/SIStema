class Icon:
    icon_type = ''

    def __init__(self, icon):
        self.icon = icon

    def __str__(self):
        return '%s %s-%s' % (self.icon_type, self.icon_type, self.icon)


class FaIcon(Icon):
    icon_type = 'fa'


class GlyphIcon(Icon):
    icon_type = 'glyphicon'
