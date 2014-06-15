"""Project management."""

import os
import shutil
import pygit2

from sundara.jala import Jala
from sundara import resources
from sundara import config
from sundara.tools import config2kwargs

class Project():
    def __init__(self, dir):
        self.dir = dir
        self.index = 'index'
        self.header = 'header'
        self.footer = 'footer'
        self.nav = 'nav'
        self.md_ext = '.md'
        self.html_ext = '.html'
        self.skip = [
                self.header + self.md_ext,
                self.footer + self.md_ext,
                self.nav + self.md_ext,
                self.md_ext,  # Ignore files named '.md'.
        ]

        conf_file = os.path.join(self.dir, config.PROJECT_CONF)
        if os.path.exists(conf_file):
            self.config = config.Config(self.dir)
            self.md_dir = self.config.get('sundara', 'md')
            self.generate_path = os.path.join(self.dir,
                    self.config.get('sundara', 'generate'))
            self.css_path = self.config.get('sundara', 'css')
            self.js_path = self.config.get('sundara', 'js')
        else:
            self.md_dir = 'md/'
            self.generate_path = os.path.join(self.dir, 'www/')
            self.css_path = 'css/'
            self.js_path = 'js/'

        self.md_path = os.path.join(self.dir, self.md_dir)

    def get_stylesheets(self):
        repo = pygit2.Repository(self.dir)
        return [ f.path[len(self.css_path):] for f in repo.index if (
            f.path.endswith('.css') and f.path.startswith(self.css_path)) ]

    def get_javascript(self):
        repo = pygit2.Repository(self.dir)
        return [ f.path[len(self.js_path):] for f in repo.index if (
            f.path.endswith('.js') and f.path.startswith(self.js_path)) ]

    def get_header(self):
        header = self.header + self.md_ext
        if header in self.get_files():
            with open(os.path.join(self.md_path, header), "r") as md:
                return md.read()
        else:
            return str()

    def get_footer(self):
        footer = self.footer + self.md_ext
        if footer in self.get_files():
            with open(os.path.join(self.md_path, footer), "r") as md:
                return md.read()
        else:
            return str()

    def get_nav(self):
        nav = self.nav + self.md_ext
        if nav in self.get_files():
            with open(os.path.join(self.md_path, nav), "r") as md:
                return md.read()
        else:
            return str()

    def get_files(self):
        repo = pygit2.Repository(self.dir)
        return [ f.path[len(self.md_dir):] for f in repo.index if (f.path.endswith(self.md_ext)
                and f.path.startswith(self.md_dir)) ]

    def generate(self):
        # Clean up the generation directory.
        
        # TODO: This entire block will be removed in refactoring.
        try:
            shutil.rmtree(self.generate_path)
            os.makedirs(self.generate_path)
        except OSError:
            os.makedirs(self.generate_path)

        jala_args = config2kwargs(self.config.config)
        jala_args.update({
            'dir': self.dir,
            'header': self.get_header(),
            'nav': self.get_nav(),
            'footer': self.get_footer(),
        })
        jala = Jala(**jala_args)
        for file in self.get_files():
            if file not in self.skip:
                # Find the filename for the generated HTML, and convert.
                if file == os.path.join(self.index + self.md_ext):
                    html = jala.convert(open(os.path.join(self.md_path,
                        file)).read(), homepage=True)
                    newfilename = os.path.join(self.generate_path, self.index + self.html_ext)
                else:
                    html = jala.convert(open(os.path.join(self.md_path, file)).read())
                    newfilename = os.path.join(self.generate_path,
                            file[:-len(self.md_ext)], self.index + self.html_ext)
                    dir = os.path.dirname(newfilename)
                    if dir != '' and not os.path.exists(dir):
                        os.makedirs(dir)

                # Write the generated file.
                with open(newfilename, "w+") as newfile:
                    newfile.write(html)

    def init(self):
        pygit2.init_repository(self.dir)
        for dir in [ self.md_path, self.generate_path ]:
            try:
                os.makedirs(dir)
            except OSError:
                # Dir exists, so we don't need to create it.
                pass
        self.config = config.Config(self.dir)
        for file in resources.INIT_FILES:
            if not os.path.exists(os.path.join(self.dir, file)):
                with open(os.path.join(self.dir, file), "w+") as f:
                    f.write(resources.INIT_FILES[file])