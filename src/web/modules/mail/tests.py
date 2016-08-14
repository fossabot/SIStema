from django.test import TestCase

from . import views
from .models import EmailMessage, ExternalEmailUser


class EmailCitationTests(TestCase):

    def test_simple_depth_one_citing(self):
        """
        Just a simple depth one citing test
        """
        text = 'Hello, I am a message'
        expected_response = '> Hello, I am a message'
        self.assertEqual(views.cite_text(text), expected_response)

    def test_simple_depth_two_citing(self):
        """
        Just a simple depth two citing test
        """
        text = 'Hello, I am a message\n> And this is cited text'
        expected_response = '> Hello, I am a message\n>> And this is cited text'
        self.assertEqual(views.cite_text(text), expected_response)

    def test_long_words(self):
        """
        Long words should not be split
        """
        text = 'Thisisaverylongwordthatisgonnamesswiththespellingcheckandwithyourbrain.'
        expected_response = '> Thisisaverylongwordthatisgonnamesswiththespellingcheckandwithyourbrain.'
        self.assertEqual(views.cite_text(text), expected_response)

    def test_lines_starting_with_bigger(self):
        """
        A space followed by > shouldn't be counted as citing
        """
        text = ' >..<>..<>..<'
        expected_response = '> >..<>..<>..<'
        self.assertEqual(views.cite_text(text), expected_response)

    def test_lines_starting_with_bigger_depth_two(self):
        """
        A space followed by > shouldn't be counted as citing (Depth two)
        """
        text = '> >..<>..<>..<'
        expected_response = '>> >..<>..<>..<'
        self.assertEqual(views.cite_text(text), expected_response)

    def test_inserted_line_breaks(self):
        """
        Line breaks should be inserted instead of spaces
        !!! If you change MAX_STRING_LENGTH you might have to change this test as well !!!
        """
        text = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaa'
        expected_text = '> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n> aaaaaaaaaaaaaa'
        self.assertEqual(views.cite_text(text), expected_text)

    def test_inserted_line_breaks_after_long_word(self):
        """
        If a word is too long the line should be broken in the first possible place after it
        !!! If you change MAX_STRING_LENGTH you might have to change this test as well !!!
        """
        text = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaa'
        expected_text = '> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n> aaaaaaaaaa'
        self.assertEqual(views.cite_text(text), expected_text)


class PageNumberTests(TestCase):

    def test_simple_correct_usage(self):
        """
        Testing a correct page number
        """
        page_input = "2"
        expected_result = (False, 2)  # do_redirect=False, page_index=2
        self.assertEqual(views._read_page_index(page_input, 2 * views.EMAILS_PER_PAGE), expected_result)

    def test_too_big(self):
        """
        If the page index is too big you should be redirected to the last page
        """
        page_input = "3"
        expected_result = (True, 2)
        self.assertEqual(views._read_page_index(page_input, 2 * views.EMAILS_PER_PAGE), expected_result)

    def test_too_small(self):
        """
        If the page index is too small you should be redirected to the first page
        """
        page_input = "-1"
        expected_result = (True, 1)
        self.assertEqual(views._read_page_index(page_input, 2 * views.EMAILS_PER_PAGE), expected_result)

    def test_float(self):
        """
        If the page index is a float you should be redirected to the first page
        """
        page_input = "2.5"
        expected_result = (True, 1)
        self.assertEqual(views._read_page_index(page_input, 2 * views.EMAILS_PER_PAGE), expected_result)

    def test_non_decimal(self):
        """
        If the page index is not a decimal or integer you should be redirected to the first page
        """
        page_input = "abacaba"
        expected_result = (True, 1)
        self.assertEqual(views._read_page_index(page_input, 2 * views.EMAILS_PER_PAGE), expected_result)

    def test_float_inf(self):
        """
        If the page index is "inf" or "-inf" etc. you should be redirected to the first page
        """
        page_input = "inf"
        expected_result = (True, 1)
        self.assertEqual(views._read_page_index(page_input, 2 * views.EMAILS_PER_PAGE), expected_result)

    def test_nan_string(self):
        """
        If the page index is "nan" you should be redirected to the first page
        """
        page_input = "nan"
        expected_result = (True, 1)
        self.assertEqual(views._read_page_index(page_input, 2 * views.EMAILS_PER_PAGE), expected_result)


class EmailMessageHtmlCleaningTests(TestCase):
    def setUp(self):
        sender = ExternalEmailUser(email='test@test.ru', display_name='John Doe')
        sender.save()
        self.message = EmailMessage(sender=sender)

    def test_escape_javascript_block(self):
        self.message.html_text = "<script>alert('XSS');</script>"
        self.message.save()
        self.assertEqual(self.message.html_text, '&lt;script&gt;alert(\'XSS\');&lt;/script&gt;')

    def test_not_escape_text_format(self):
        self.message.html_text = "<b>Hi!</b><i>Lol</i>"
        self.message.save()
        self.assertEqual(self.message.html_text, '<b>Hi!</b><i>Lol</i>')

    def test_escape_inline_xss(self):
        self.message.html_text = "<IMG SRC=\"javascript:alert(\'XSS\');\">"
        self.message.save()
        self.assertEqual(self.message.html_text, '&lt;img src="javascript:alert(\'XSS\');"&gt;')

    def test_case_sensitive_xss(self):
        self.message.html_text = "<IMG SRC=JaVaScRiPt:alert('XSS')>"
        self.message.save()
        self.assertEqual(self.message.html_text, '&lt;img src="JaVaScRiPt:alert(\'XSS\')"&gt;')

    def test_escape_onclick(self):
        self.message.html_text = "<img onclick>"
        self.message.save()
        self.assertEqual(self.message.html_text, '&lt;img onclick=""&gt;')

    def test_escape_nesting_script(self):
        self.message.html_text = "<<script>script> alert(\"XSS.\"); </</script>script>"
        self.message.save()
        self.assertEqual(self.message.html_text, '&lt;&lt;script&gt;script&gt; alert("XSS."); script&gt;')

    def test_escape_style_tag(self):
        self.message.html_text = "<b style='position: 0 0;'>Hello</b>"
        self.message.save()
        self.assertEqual(self.message.html_text, '<b>Hello</b>')

    def test_large_mail(self):
        self.message.html_text = "<script>alert('XSS');</script>" * 5000
        self.message.save()
        self.assertEqual(self.message.html_text, '&lt;script&gt;alert(\'XSS\');&lt;/script&gt;' * 5000)
