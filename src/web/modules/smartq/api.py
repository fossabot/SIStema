# Answer fields:
# - one line text
# - multiline text
# - number
#
# - format string
class GeneratedQuestionData:
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

        if getattr(self, 'answer_fields', None) is None:
            # TODO: Add one-line field without verification
            self.answer_fields = []
