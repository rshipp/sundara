import unittest

from sundara import jala

class TestJala(unittest.TestCase):

    def setUp(self):
        self.valid_md = "# This is an h1.\n\n" \
                        "This is some text inside a <p>.\nAnd more text.\n\n" \
                        "* This is a list item.\n"

    def tearDown(self):
        pass

    def produces_correct_html(self, j, name, should_have_div=True):
        html = str(j.cache[name]).strip()
        self.assertTrue(html.startswith('<'+name+''))
        self.assertIn('This is an h1.', html)
        if should_have_div:
            self.assertIn('<div', html)
            self.assertIn('</div>', html)
        else:
            self.assertNotIn('<div', html)
            self.assertNotIn('</div>', html)
        self.assertTrue(html.endswith('</'+name+'>'))


    def test_convert_header_produces_correct_html(self):
        j = jala.Jala()
        j.convert_header(self.valid_md)
        self.produces_correct_html(j, 'header')

    def test_convert_footer_produces_correct_html(self):
        j = jala.Jala()
        j.convert_footer(self.valid_md)
        self.produces_correct_html(j, 'footer')

    def test_convert_nav_produces_correct_html(self):
        j = jala.Jala()
        j.convert_nav(self.valid_md)
        self.produces_correct_html(j, 'nav', should_have_div=False)
