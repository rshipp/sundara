"""Sundara jāla: for a beautiful web.
Convert markdown to clean HTML5.
"""

import os
import sys
import shutil
import re
from markdown import Markdown
from bs4 import BeautifulSoup
import pygit2

DOCTYPE="<!DOCTYPE html>\n"

class Jala():
    """Convert Markdown to clean, properly formatted HTML5."""
    def __init__(self, sundara):
        self.sundara = sundara
        self.config = self.sundara.config
        self.css_path = self.config.get('sundara', 'css')
        self.js_path = self.config.get('sundara', 'js')
        self.style_css_path = self.config.get('style', 'css')
        self.style_js_path = self.config.get('style', 'js')
        if os.path.isabs(self.style_css_path):
            self.style_css = self.style_css_path[1:]
        else:
            self.style_css = self.style_css_path
        if os.path.isabs(self.style_js_path):
            self.style_js = self.style_js_path[1:]
        else:
            self.style_js = self.style_js_path

    def get_stylesheets(self):
        repo = pygit2.Repository(self.sundara.dir)
        return [ f.path[len(self.css_path):] for f in repo.index if (
            f.path.endswith('.css') and f.path.startswith(self.css_path)) ]

    def get_javascript(self):
        repo = pygit2.Repository(self.sundara.dir)
        return [ f.path[len(self.js_path):] for f in repo.index if (
            f.path.endswith('.js') and f.path.startswith(self.js_path)) ]

    def get_header(self):
        header = self.sundara.header + self.sundara.md_ext
        if header in self.sundara.get_files():
            with open(os.path.join(self.sundara.md_path, header), "r") as md:
                return md.read()
        else:
            return str()

    def get_footer(self):
        footer = self.sundara.footer + self.sundara.md_ext
        if footer in self.sundara.get_files():
            with open(os.path.join(self.sundara.md_path, footer), "r") as md:
                return md.read()
        else:
            return str()

    def get_nav(self):
        nav = self.sundara.nav + self.sundara.md_ext
        if nav in self.sundara.get_files():
            with open(os.path.join(self.sundara.md_path, nav), "r") as md:
                return md.read()
        else:
            return str()

    def convert(self, md, homepage=False):
        markdown = Markdown(output_format="html5")

        # Form the HTML document.
        main = BeautifulSoup().new_tag('div',
            id=self.config.get('content', 'main'))
        # Header
        header = self.get_header()
        if header != '':
            htag1 = BeautifulSoup().new_tag('header',
                    role=self.config.get('content', 'header_role'))
            htag1['class'] = self.config.get('content', 'header')
            main.append(htag1)
            htag2 = BeautifulSoup().new_tag('div')
            htag2['class'] = self.config.get('content', 'header_content')
            main.header.append(htag2)
            bh = BeautifulSoup(markdown.convert(header), "html5lib")
            bh.html.unwrap()
            bh.body.unwrap()
            bh.head.extract()
            main.header.div.append(bh)
        # Nav
        nav = self.get_nav()
        if nav != '':
            ntag = BeautifulSoup().new_tag('nav',
                    role=self.config.get('content', 'nav_role'))
            ntag['class'] = self.config.get('content', 'nav')
            main.append(ntag)
            bn = BeautifulSoup(markdown.convert(nav), "html5lib")
            bn.html.unwrap()
            bn.body.unwrap()
            bn.head.extract()
            main.nav.append(bn)
        # Content
        bc = BeautifulSoup(markdown.convert(md), "html5lib")
        bc.html.unwrap()
        ctag1 = BeautifulSoup().new_tag('div')
        ctag1['class'] = self.config.get('content', 'container')
        bc.body.wrap(ctag1)
        ctag2 = BeautifulSoup().new_tag('div')
        ctag2['class'] = self.config.get('content', 'row')
        bc.body.wrap(ctag2)
        ctag3 = BeautifulSoup().new_tag('div')
        ctag3['class'] = self.config.get('content', 'content')
        bc.body.wrap(ctag3)
        bc.body.unwrap()
        bc.head.extract()
        main.append(bc)
        # Footer
        footer = self.get_footer()
        if footer != '':
            ftag1 = BeautifulSoup().new_tag('footer')
            ftag1['class'] = self.config.get('content', 'footer')
            main.append(ftag1)
            ftag2 = BeautifulSoup().new_tag('div')
            ftag2['class'] = self.config.get('content', 'footer_content')
            main.footer.append(ftag2)
            bf = BeautifulSoup(markdown.convert(footer), "html5lib")
            bf.html.unwrap()
            bf.body.unwrap()
            main.footer.div.append(bf)
            bf.head.extract()
        # Throw it all in the soup!
        soup = BeautifulSoup(DOCTYPE, "html5lib")
        soup.body.append(main)

        # Add meta information.
        soup.html['lang'] = self.config.get('meta', 'lang')
        soup.head.append(BeautifulSoup().new_tag('meta',
            charset=self.config.get('meta', 'encoding')))
        soup.head.append(BeautifulSoup().new_tag('title'))
        # Parse out the title formatter.
        site_name = self.config.get('meta', 'name')
        if homepage:
            soup.title.string = site_name
        else:
            soup.title.string = self.config.get('meta',
                    'title').replace('{name}', site_name).replace('{h1}',
                            soup.h1.string)
        # If description exists, add it to the homepage ONLY.
        if homepage and self.config.get('meta', 'description') != '':
                desc = BeautifulSoup().new_tag('meta',
                        content=self.config.get('meta', 'description'))
                desc['name'] = 'description'
                soup.head.append(desc)

        # Link in Bootstrap and jQuery.
        if self.config.get('style', 'bootstrap') == 'on':
            soup.head.append(BeautifulSoup().new_tag('link', rel='stylesheet',
                href='//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css'))
            soup.body.append(BeautifulSoup().new_tag('script',
                src='//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'))
        if self.config.get('style', 'jquery') == 'on':
            soup.body.append(BeautifulSoup().new_tag('script',
                src='//code.jquery.com/jquery-1.11.0.min.js'))

        # Add custom CSS and JS.
        stylesheets = self.get_stylesheets()
        for stylesheet in stylesheets:
            # Link the file.
            soup.head.append(BeautifulSoup().new_tag('link', rel='stylesheet',
                href=os.path.join(self.style_css_path, stylesheet)))
            # Install the file.
            os.makedirs(os.path.join(self.sundara.generate_path,
                self.css_path))
            shutil.copy(os.path.join(self.sundara.dir, self.css_path,
                stylesheet), os.path.join(self.sundara.generate_path,
                    self.style_css, stylesheet))
        scripts = self.get_javascript()
        for script in scripts:
            # Link the file.
            soup.body.append(BeautifulSoup().new_tag('script',
                src=os.path.join(self.style_js_path, script)))
            # Install the file.
            os.makedirs(os.path.join(self.sundara.generate_path,
                self.js_path))
            shutil.copy(os.path.join(self.sundara.dir, self.js_path,
                script), os.path.join(self.sundara.generate_path,
                        self.style_js, script))

        # Prettify and split.
        html = soup.prettify().split('\n')

        # Fix indentation for non-tag lines.
        for index, line in enumerate(html):
            if index > 0 and re.match("\s*[^<\s]", line) and re.match("\s+[^<\s]", html[index - 1]):
                # if line isn't a tag and previous line is indented and not a tag
                html[index] = re.match("\s*", html[index - 1]).group() + line

        return BeautifulSoup('\n'.join(html)).prettify()
