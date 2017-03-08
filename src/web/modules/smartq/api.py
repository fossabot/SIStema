import enum

class Generator:
    def generate(self):
        raise NotImplementedError()


# TODO: think of the way to return a message along with the status
# TODO: it's also useful to return error messages to the specific cells as well
#       as error message to the whole form
class Checker:
    # TODO: better names?
    class Result(enum.IntEnum):
        # Use explicit values and don't change the existing ones. That's
        # important because they are stored in the database.
        OK = 1
        WA = 2
        PE = 3

    def __init__(self):
        self.message = ''

    def check(self, generated_question_data, answer):
        raise NotImplementedError()


class GeneratedQuestionData:
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

        if getattr(self, 'answer_fields', None) is None:
            # TODO: Add one-line field without verification
            self.answer_fields = []


# TODO: is there a better name?
class AnswerFieldSpec:
    class Type(enum.IntEnum):
        # Use explicit values and don't change the existing ones. That's
        # important because they are stored in the database.
        TEXT = 1
        INTEGER = 2

    @classmethod
    def text(cls, multiline=False, validation_regexp=None):
        # TODO: min_length, max_length?
        # TODO: what about using enum?
        spec = {'type': cls.Type.TEXT}

        if not isinstance(multiline, bool):
            raise Exception('multiline must be either True or False')

        spec['multiline'] = multiline

        # TODO: can we avoid code duplication?
        if validation_regexp is not None:
            # TODO: what about trying to compile?
            if not isinstance(validation_regexp, str):
                # TODO: what kind of exception to use?
                raise Exception('validation_regexp must be a string')
            spec['validation_regexp'] = validation_regexp

        return spec

    @classmethod
    def integer(cls, min_value=None, max_value=None, **kwargs):
        spec = cls.text(**kwargs)
        spec['type'] = cls.Type.INTEGER

        if min_value is not None:
            # TODO: use an assertion instead?
            if not isinstance(min_value, int):
                # TODO: what kind of exception to use?
                raise Exception('min_value must be an integer')
            spec['min_value'] = min_value

        if max_value is not None:
            # TODO: use an assertion instead?
            if not isinstance(max_value, int):
                # TODO: what kind of exception to use?
                raise Exception('max_value must be an integer')
            spec['max_value'] = max_value

        return spec

# TODO: checker statuses
