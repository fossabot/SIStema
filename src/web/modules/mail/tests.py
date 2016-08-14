from django.test import TestCase

from . import views


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