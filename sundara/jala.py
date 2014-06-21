import os
import shutil
import re

from markdown import Markdown
import bs4

DOCTYPE="<!DOCTYPE html>\n"

class Jala():
    """Convert Markdown to clean, properly formatted HTML5."""
    def __init__(self, **kwargs):
        self.config = kwargs
        self.style_css_path = self.config.get('style.css', '/css/')
        self.style_js_path = self.config.get('style.js', '/js/')

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
        self.soup = bs4.BeautifulSoup(DOCTYPE, "html5lib")

        # Form the HTML document.
        main = bs4.BeautifulSoup().new_tag('div', id='main')
        
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

    def _new_tag(self, name, parent=None):
        config_section = ''.join(['content.', parent or '', name, '.'])
        matching_config = (
            option.lstrip(config_section)
            for option in self.config
            if option.startswith(config_section)
        )
        return bs4.BeautifulSoup().new_tag(
            name,
            **{
                key: value
                for key, value in matching_config
            }
        )

    def _convert_file(self, content, name):
        """Convert markdown to a bs4 object, and save it to the cache."""
        config_section = ''.join(['content.', name, '.'])
        tag = self._new_tag(name)
        div = self._new_tag('div', name)
        tag.append(div)
        html = bs4.BeautifulSoup(self.markdown.convert(content), "html5lib")
        for child in html.body.children:
            div.append(child)
        self.cache[name] = tag

    def convert_header(self, header):
        """Convert the header to a bs4 object, and save it to the cache."""
        self._convert_file(header, 'header')

    def convert_nav(self):
        """Convert the nav to a bs4 object, and save it to the cache."""
        ntag = self._new_tag('nav')
        bn = bs4.BeautifulSoup(self.markdown.convert(nav), "html5lib")
        bn.html.unwrap()
        bn.body.unwrap()
        bn.head.extract()
        ntag.append(bn)
        self.cache['nav'] = ntag

    def convert_content(self, md):
        """Convert the content to a bs4 object, and return it."""
        bc = bs4.BeautifulSoup(self.markdown.convert(md), "html5lib")
        bc.html.unwrap()
        ctag1 = self._new_tag('div', 'container')
        bc.body.wrap(ctag1)
        ctag2 = self._new_tag('div', 'row')
        bc.body.wrap(ctag2)
        ctag3 = self._new_tag('div', 'content')
        bc.body.wrap(ctag3)
        bc.body.unwrap()
        bc.head.extract()
        return bc

    def convert_footer(self, footer):
        """Convert the footer to a bs4 object, and save it to the cache."""
        self._convert_file(footer, 'footer')

    def add_meta(self, homepage=False):
        # Add meta information.
        self.soup.html['lang'] = self.config.get('meta.lang', 'en')
        self.soup.head.append(bs4.BeautifulSoup().new_tag('meta',
            charset=self.config.get('meta.encoding', 'utf-8')))
        self.soup.head.append(bs4.BeautifulSoup().new_tag('title'))
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
            desc = bs4.BeautifulSoup().new_tag('meta',
                    content=self.config.get('meta.description'))
            desc['name'] = 'description'
            self.soup.head.append(desc)

    def add_style(self):
        # Link in Bootstrap and jQuery.
        if self.config.get('style.jquery') == 'on':
            self.soup.body.append(bs4.BeautifulSoup().new_tag('script',
                src='//code.jquery.com/jquery-1.11.0.min.js'))
        if self.config.get('style.bootstrap') == 'on':
            self.soup.head.append(bs4.BeautifulSoup().new_tag('link', rel='stylesheet',
                href='//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css'))
            self.soup.body.append(bs4.BeautifulSoup().new_tag('script',
                src='//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'))

        # Add custom CSS and JS.
        stylesheets = self.config.get('stylesheets', [])
        for stylesheet in stylesheets:
            # Link the file.
            self.soup.head.append(bs4.BeautifulSoup().new_tag('link', rel='stylesheet',
                href=os.path.join(self.style_css_path, stylesheet)))

        scripts = self.config.get('javascript', [])
        for script in scripts:
            # Link the file.
            self.soup.body.append(bs4.BeautifulSoup().new_tag('script',
                src=os.path.join(self.style_js_path, script)))

    def prettify(self):
        # Prettify and split.
        html = self.soup.prettify().split('\n')

        # Fix indentation for non-tag lines.
        for index, line in enumerate(html):
            if index > 0 and re.match("\s*[^<\s]", line) and re.match("\s+[^<\s]", html[index - 1]):
                # if line isn't a tag and previous line is indented and not a tag
                html[index] = re.match("\s*", html[index - 1]).group() + line

        return bs4.BeautifulSoup('\n'.join(html)).prettify()
