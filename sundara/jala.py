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
        self.css_path = self.config.get('sundara.css', 'css/')
        self.js_path = self.config.get('sundara.js', 'js/')
        self.style_css_path = self.config.get('style.css', '/css/')
        self.style_js_path = self.config.get('style.js', '/js/')
        self.generate_path = self.config.get('sundara.generate')
        self.dir = self.config.get('dir')

        if os.path.isabs(self.style_css_path):
            self.style_css = self.style_css_path[1:]
        else:
            self.style_css = self.style_css_path
        if os.path.isabs(self.style_js_path):
            self.style_js = self.style_js_path[1:]
        else:
            self.style_js = self.style_js_path

    def convert(self, md, homepage=False):
        markdown = Markdown(output_format="html5")

        # Form the HTML document.
        main = BeautifulSoup().new_tag('div',
            id=self.config.get('content.main', 'main'))
        # Header
        header = self.config.get('header', '')
        if header != '':
            htag1 = BeautifulSoup().new_tag('header',
                    role=self.config.get('content.header_role', ''))
            htag1['class'] = self.config.get('content.header', '')
            main.append(htag1)
            htag2 = BeautifulSoup().new_tag('div')
            htag2['class'] = self.config.get('content.header_content', '')
            main.header.append(htag2)
            bh = BeautifulSoup(markdown.convert(header), "html5lib")
            bh.html.unwrap()
            bh.body.unwrap()
            bh.head.extract()
            main.header.div.append(bh)
        # Nav
        nav = self.config.get('nav', '')
        if nav != '':
            ntag = BeautifulSoup().new_tag('nav',
                    role=self.config.get('content.nav_role'))
            ntag['class'] = self.config.get('content.nav', '')
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
        main.append(bc)
        # Footer
        footer = self.config.get('footer', '')
        if footer != '':
            ftag1 = BeautifulSoup().new_tag('footer')
            ftag1['class'] = self.config.get('content.footer', '')
            main.append(ftag1)
            ftag2 = BeautifulSoup().new_tag('div')
            ftag2['class'] = self.config.get('content.footer_content', '')
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
        soup.html['lang'] = self.config.get('meta.lang', 'en')
        soup.head.append(BeautifulSoup().new_tag('meta',
            charset=self.config.get('meta.encoding', 'utf-8')))
        soup.head.append(BeautifulSoup().new_tag('title'))
        # Parse out the title formatter.
        site_name = self.config.get('meta.name', '')
        if homepage:
            soup.title.string = site_name
        else:
            if soup.h1:
                h1_title = soup.h1.string
            else:
                h1_title = ''
            soup.title.string = self.config.get('meta.title', '').replace(
                    '{name}', site_name).replace('{h1}', h1_title)
        # If description exists, add it to the homepage ONLY.
        if homepage and self.config.get('meta.description', '') != '':
                desc = BeautifulSoup().new_tag('meta',
                        content=self.config.get('meta.description'))
                desc['name'] = 'description'
                soup.head.append(desc)

        # Link in Bootstrap and jQuery.
        if self.config.get('style.bootstrap') == 'on':
            soup.head.append(BeautifulSoup().new_tag('link', rel='stylesheet',
                href='//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css'))
            soup.body.append(BeautifulSoup().new_tag('script',
                src='//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'))
        if self.config.get('style.jquery') == 'on':
            soup.body.append(BeautifulSoup().new_tag('script',
                src='//code.jquery.com/jquery-1.11.0.min.js'))

        # Add custom CSS and JS.
        stylesheets = self.config.get('stylesheets', [])
        for stylesheet in stylesheets:
            # Link the file.
            soup.head.append(BeautifulSoup().new_tag('link', rel='stylesheet',
                href=os.path.join(self.style_css_path, stylesheet)))
            # Install the file.
            os.makedirs(os.path.join(self.generate_path,
                self.css_path))
            shutil.copy(os.path.join(self.dir, self.css_path,
                stylesheet), os.path.join(self.generate_path,
                    self.style_css, stylesheet))
        scripts = self.config.get('javascript', [])
        for script in scripts:
            # Link the file.
            soup.body.append(BeautifulSoup().new_tag('script',
                src=os.path.join(self.style_js_path, script)))
            # Install the file.
            os.makedirs(os.path.join(self.generate_path,
                self.js_path))
            shutil.copy(os.path.join(self.dir, self.js_path,
                script), os.path.join(self.generate_path,
                        self.style_js, script))

        # Prettify and split.
        html = soup.prettify().split('\n')

        # Fix indentation for non-tag lines.
        for index, line in enumerate(html):
            if index > 0 and re.match("\s*[^<\s]", line) and re.match("\s+[^<\s]", html[index - 1]):
                # if line isn't a tag and previous line is indented and not a tag
                html[index] = re.match("\s*", html[index - 1]).group() + line

        return BeautifulSoup('\n'.join(html)).prettify()
