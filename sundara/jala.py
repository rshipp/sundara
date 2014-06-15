import os
import shutil
import re

from markdown import Markdown
from bs4 import BeautifulSoup

DOCTYPE="<!DOCTYPE html>\n"

class Jala():
    """Convert Markdown to clean, properly formatted HTML5."""
    def __init__(self, **kwargs):
        self.config = kwargs
        self.style_css_path = self.config.get('style.css', '/css/')
        self.style_js_path = self.config.get('style.js', '/js/')

        # These need to be refactored out.
        self.css_path = self.config.get('sundara.css', 'css/')
        self.js_path = self.config.get('sundara.js', 'js/')
        self.generate_path = self.config.get('sundara.generate')
        self.dir = self.config.get('dir')
        # ^^^^

        if os.path.isabs(self.style_css_path):
            self.style_css = self.style_css_path[1:]
        else:
            self.style_css = self.style_css_path
        if os.path.isabs(self.style_js_path):
            self.style_js = self.style_js_path[1:]
        else:
            self.style_js = self.style_js_path

        # Cache some values in memory for faster conversion.
        self.cache = {
            'header': None,
            'nav': None,
            'footer': None,
        }
        self.fn_map = {
            'header': self.convert_header,
            'nav': self.convert_nav,
            'footer': self.convert_footer,
        }
        self.soup = None
        self.markdown = Markdown(output_format="html5")

    def convert(self, md, homepage=False):
        self.soup = BeautifulSoup(DOCTYPE, "html5lib")

        # Form the HTML document.
        main = BeautifulSoup().new_tag('div',
            id=self.config.get('content.main', 'main'))
        
        # Convert the header/footer/nav, if they exist.
        for section in self.fn_map:
            if self.cache[section] is None:
                content = self.config.get(section, '')
                if content:
                    self.fn_map[section](content)
                else:
                    self.cache[section] = ''

        # Add each section to the `main` div in order.
        main.append(self.cache['header'])
        main.append(self.cache['nav'])
        main.append(self.convert_content(md))
        main.append(self.cache['footer'])

        # Throw it all in the soup!
        self.soup.body.append(main)
        # Set up metadata and style.
        self.add_meta(homepage)
        self.add_style()
        # Prettify and return.
        return self.prettify()

    def convert_header(self, header):
        """Convert the header to a bs4 object, and save it to the cache."""
        htag1 = BeautifulSoup().new_tag('header',
                role=self.config.get('content.header_role', ''))
        htag1['class'] = self.config.get('content.header', '')
        htag2 = BeautifulSoup().new_tag('div')
        htag2['class'] = self.config.get('content.header_content', '')
        htag1.append(htag2)
        bh = BeautifulSoup(self.markdown.convert(header), "html5lib")
        bh.html.unwrap()
        bh.body.unwrap()
        bh.head.extract()
        htag2.append(bh)
        self.cache['header'] = htag1

    def convert_nav(self):
        """Convert the nav to a bs4 object, and save it to the cache."""
        ntag = BeautifulSoup().new_tag('nav',
                role=self.config.get('content.nav_role'))
        ntag['class'] = self.config.get('content.nav', '')
        bn = BeautifulSoup(self.markdown.convert(nav), "html5lib")
        bn.html.unwrap()
        bn.body.unwrap()
        bn.head.extract()
        ntag.append(bn)
        self.cache['nav'] = ntag

    def convert_content(self, md):
        """Convert the content to a bs4 object, and return it."""
        bc = BeautifulSoup(self.markdown.convert(md), "html5lib")
        bc.html.unwrap()
        ctag1 = BeautifulSoup().new_tag('div')
        ctag1['class'] = self.config.get('content.container', '')
        bc.body.wrap(ctag1)
        ctag2 = BeautifulSoup().new_tag('div', '')
        ctag2['class'] = self.config.get('content.row', '')
        bc.body.wrap(ctag2)
        ctag3 = BeautifulSoup().new_tag('div')
        ctag3['class'] = self.config.get('content.content', '')
        bc.body.wrap(ctag3)
        bc.body.unwrap()
        bc.head.extract()
        return bc

    def convert_footer(self):
        """Convert the footer to a bs4 object, and save it to the cache."""
        ftag1 = BeautifulSoup().new_tag('footer')
        ftag1['class'] = self.config.get('content.footer', '')
        ftag2 = BeautifulSoup().new_tag('div')
        ftag2['class'] = self.config.get('content.footer_content', '')
        ftag1.append(ftag2)
        bf = BeautifulSoup(self.markdown.convert(footer), "html5lib")
        bf.html.unwrap()
        bf.body.unwrap()
        bf.head.extract()
        ftag2.append(bf)
        self.cache['footer'] = ftag1

    def add_meta(self, homepage=False):
        # Add meta information.
        self.soup.html['lang'] = self.config.get('meta.lang', 'en')
        self.soup.head.append(BeautifulSoup().new_tag('meta',
            charset=self.config.get('meta.encoding', 'utf-8')))
        self.soup.head.append(BeautifulSoup().new_tag('title'))
        # Parse out the title formatter.
        site_name = self.config.get('meta.name', '')
        if homepage:
            self.soup.title.string = site_name
        else:
            if self.soup.h1:
                h1_title = self.soup.h1.string
            else:
                h1_title = ''
            self.soup.title.string = self.config.get('meta.title', '').replace(
                    '{name}', site_name).replace('{h1}', h1_title)
        # If description exists, add it to the homepage ONLY.
        if homepage and self.config.get('meta.description', '') != '':
            desc = BeautifulSoup().new_tag('meta',
                    content=self.config.get('meta.description'))
            desc['name'] = 'description'
            self.soup.head.append(desc)

    def add_style(self):
        # Link in Bootstrap and jQuery.
        if self.config.get('style.bootstrap') == 'on':
            self.soup.head.append(BeautifulSoup().new_tag('link', rel='stylesheet',
                href='//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css'))
            self.soup.body.append(BeautifulSoup().new_tag('script',
                src='//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'))
        if self.config.get('style.jquery') == 'on':
            self.soup.body.append(BeautifulSoup().new_tag('script',
                src='//code.jquery.com/jquery-1.11.0.min.js'))

        # Add custom CSS and JS.
        stylesheets = self.config.get('stylesheets', [])
        for stylesheet in stylesheets:
            # Link the file.
            self.soup.head.append(BeautifulSoup().new_tag('link', rel='stylesheet',
                href=os.path.join(self.style_css_path, stylesheet)))

            # This needs to be refactored out.
            # Install the file.
            os.makedirs(os.path.join(self.generate_path,
                self.css_path))
            shutil.copy(os.path.join(self.dir, self.css_path,
                stylesheet), os.path.join(self.generate_path,
                    self.style_css, stylesheet))
            # ^^^^

        scripts = self.config.get('javascript', [])
        for script in scripts:
            # Link the file.
            self.soup.body.append(BeautifulSoup().new_tag('script',
                src=os.path.join(self.style_js_path, script)))

            # This needs to be refactored out.
            # Install the file.
            os.makedirs(os.path.join(self.generate_path,
                self.js_path))
            shutil.copy(os.path.join(self.dir, self.js_path,
                script), os.path.join(self.generate_path,
                        self.style_js, script))
            # ^^^^

    def prettify(self):
        # Prettify and split.
        html = self.soup.prettify().split('\n')

        # Fix indentation for non-tag lines.
        for index, line in enumerate(html):
            if index > 0 and re.match("\s*[^<\s]", line) and re.match("\s+[^<\s]", html[index - 1]):
                # if line isn't a tag and previous line is indented and not a tag
                html[index] = re.match("\s*", html[index - 1]).group() + line

        return BeautifulSoup('\n'.join(html)).prettify()
