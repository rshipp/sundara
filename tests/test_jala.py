import unittest

from sundara import jala

class TestJala(unittest.TestCase):

    def setUp(self):
        self.valid_md = "# This is an h1.\n\n" \
                        "This is some text inside a <p>.\nAnd more text.\n\n" \
                        "* This is a list item.\n"
        self.j = jala.Jala()

    def tearDown(self):
        pass

    def produces_correct_html(self, name, should_have_div=True):
        html = str(self.j.cache[name]).strip()
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
        self.j.convert_header(self.valid_md)
        self.produces_correct_html('header')

    def test_convert_footer_produces_correct_html(self):
        self.j.convert_footer(self.valid_md)
        self.produces_correct_html('footer')

    def test_convert_nav_produces_correct_html(self):
        self.j.convert_nav(self.valid_md)
        self.produces_correct_html('nav', should_have_div=False)

    def test_convert_uses_nav(self):
        self.j.config['nav'] = 'test'
        html = self.j.convert('content')
        self.assertIn('test', html)
        self.assertEquals('<nav><p>test</p></nav>',
                str(self.j.cache['nav']))

    def test_integration_convert_produces_correct_html(self):
        html = self.j.convert(self.valid_md).strip()
        self.assertIn('DOCTYPE', html)
        self.assertIn('<html', html)
        self.assertIn('This is an h1.', html)
        self.assertTrue(html.endswith('</html>'))

    def test_convert_adds_desc_to_index(self):
        self.j.config['meta.description'] = 'test description'
        html = self.j.convert(self.valid_md, homepage=True)
        self.assertIn('name="description"', html)
        self.assertIn('test description', html)

    def test_add_style_links_stylesheets(self):
        files = [
            '/css/test.css',
            '/css/anothertest.css',
        ]
        self.j.config['stylesheets'] = files
        html = self.j.convert('content')
        self.assertIn('<link', html)
        self.assertIn('rel="stylesheet"', html)
        self.assertIn(files[0], html)
        self.assertIn(files[1], html)

    def test_add_style_links_scripts(self):
        files = [
            '/js/test.js',
            '/js/anothertest.js',
        ]
        self.j.config['javascript'] = files
        html = self.j.convert('content')
        self.assertIn('<script', html)
        self.assertIn('src="{file}"'.format(file=files[0]), html)
        self.assertIn('src="{file}"'.format(file=files[1]), html)

    def test_convert_footer_uses_config_values(self):
        self.j.config['content.footer.class'] = 'footer'
        self.j.convert_footer('content')
        self.assertIn('<footer class="footer">', str(self.j.cache['footer']))

    def test_convert_uses_config_values(self):
        self.j.config['content.container.div.class'] = 'test'
        html = self.j.convert('content')
        self.assertIn('<div class="test">', html)
