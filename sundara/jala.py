"""Sundara jāla: for a beautiful web.
Convert markdown to clean HTML5.
"""

import os
import sys
import shutil
import re
from markdown import Markdown
from bs4 import BeautifulSoup

DOCTYPE="<!DOCTYPE html>\n"

class Jala():
    """Convert Markdown to clean, properly formatted HTML5."""
    def __init__(self, sundara):
        self.sundara = sundara
        self.config = self.sundara.config
        self.css_path = self.config.get('sundara', 'css')
        self.js_path = self.config.get('sundara', 'js')

    def get_stylesheets(self):
        repo = pygit2.Repository(self.dir)
        return [ f.path[len(self.css_path):] for f in repo.index if (
            f.path.endswith('.css') and f.path.startswith(self.css_path)) ]

    def get_javascript(self):
        repo = pygit2.Repository(self.dir)
        return [ f.path[len(self.js_path):] for f in repo.index if (
            f.path.endswith('.js') and f.path.startswith(self.js_path)) ]

    def get_header(self):
        header = self.sundara.header + self.sundara.md_ext
        if header in self.sundara.get_files()
            return header

    def get_footer(self):
        footer = self.sundara.footer + self.sundara.md_ext
        if footer in self.sundara.get_files()
            return footer

    def get_nav(self):
        nav = self.sundara.nav + self.sundara.md_ext
        if nav in self.sundara.get_files()
            return nav

    def convert(self, md, homepage=False):
        markdown = Markdown(output_format="html5")
        soup = BeautifulSoup(DOCTYPE + markdown.convert(md), "html5lib")

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
                soup.head.append(BeautifulSoup().new_tag('meta',
                    name='description', content=self.config.get('meta', 'description')))

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
                href=os.path.join(self.config.get('style', 'css'), stylesheet))
            # Install the file.
            shutil.copy(os.path.join(self.sundara.dir, self.css_path,
                stylesheet), os.path.join(self.sundara.generate_path,
                    self.config.get('style', 'css'), stylesheet))
        scripts = self.get_javascript()
        for script in scripts:
            # Link the file.
            soup.body.append(BeautifulSoup().new_tag('script',
                src=os.path.join(self.config.get('style', 'js'), script))
            # Install the file.
            shutil.copy(os.path.join(self.sundara.dir, self.js_path,
                script), os.path.join(self.sundara.generate_path,
                        self.config.get('style', 'js'), script))

        # Prettify and split.
        html = soup.prettify().split('\n')

        # Fix indentation for non-tag lines.
        for index, line in enumerate(html):
            if index > 0 and re.match("\s*[^<\s]", line) and re.match("\s+[^<\s]", html[index - 1]):
                # if line isn't a tag and previous line is indented and not a tag
                html[index] = re.match("\s*", html[index - 1]).group() + line

        return '\n'.join(html)
