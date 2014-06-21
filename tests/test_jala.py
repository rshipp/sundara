import unittest

from sundara import jala

class TestJala(unittest.TestCase):

    def setUp(self):
        self.valid_md = "# This is an h1.\n\n" \
                        "This is some text inside a <p>.\nAnd more text.\n\n" \
                        "* This is a list item.\n"

    def tearDown(self):
        pass

    def test_convert_header_produces_correct_html(self):
        j = jala.Jala()
        j.convert_header(self.valid_md)
        html = str(j.cache['header']).strip()
        self.assertTrue(html.startswith('<header'))
        self.assertIn('<div', html)
        self.assertIn('This is an h1.', html)
        self.assertIn('</div>', html)
        self.assertTrue(html.endswith('</header>'))

    def test_convert_footer_produces_correct_html(self):
        j = jala.Jala()
        j.convert_footer(self.valid_md)
        html = str(j.cache['footer']).strip()
        self.assertTrue(html.startswith('<footer'))
        self.assertIn('<div', html)
        self.assertIn('This is an h1.', html)
        self.assertIn('</div>', html)
        self.assertTrue(html.endswith('</footer>'))
