"""Project management."""

import os
import shutil
import pygit2

from sundara.jala import Jala
from sundara import resources
from sundara import config
from sundara import exceptions
from sundara.tools import config2kwargs

class Project():
    def __init__(self, project_dir):
        self.project_dir = project_dir
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

        conf_file = os.path.join(self.project_dir, config.PROJECT_CONF)
        if os.path.exists(conf_file):
            self.config = config.Config(self.project_dir)
            self.md_dir = self.config.get('sundara', 'md')
            self.generate_path = os.path.join(self.project_dir,
                    self.config.get('sundara', 'generate'))
            self.css_path = self.config.get('sundara', 'css')
            self.js_path = self.config.get('sundara', 'js')
        else:
            self.md_dir = 'md/'
            self.generate_path = os.path.join(self.project_dir, 'www/')
            self.css_path = 'css/'
            self.js_path = 'js/'

        self.md_path = os.path.join(self.project_dir, self.md_dir)

    # get_{files} methods
    # For obtaining lists of filenames.

    def _get_files(self, folder, extension):
        repo = pygit2.Repository(self.project_dir)
        return [ f.path[len(folder):] for f in repo.index if (
            f.path.endswith(extension) and f.path.startswith(folder)) ]

    def get_stylesheets(self):
        return self._get_files(self.css_path, '.css')

    def get_javascript(self):
        return self._get_files(self.js_path, '.js')

    def get_markdown(self):
        return self._get_files(self.md_dir, self.md_ext)

    # get_{file} methods
    # For obtaining the contents of a specific file.

    def _get_file(self, filename):
        name = filename + self.md_ext
        if name in self.get_markdown():
            with open(os.path.join(self.md_path, name), "r") as md:
                return md.read()
        else:
            return str()

    def get_header(self):
        return self._get_file(self.header)

    def get_footer(self):
        return self._get_file(self.footer)

    def get_nav(self):
        return self._get_file(self.nav)

    # Methods for the main project commands.

    def generate(self):
        # Clean up the generation directory.
        
        # TODO: This entire block will be removed in refactoring.
        try:
            shutil.rmtree(self.generate_path)
            os.makedirs(self.generate_path)
        except OSError:
            os.makedirs(self.generate_path)
        # ^^^

        jala_args = config2kwargs(self.config.config)
        jala_args.update({
            'header': self.get_header(),
            'nav': self.get_nav(),
            'footer': self.get_footer(),
        })
        jala = Jala(**jala_args)
        for filename in self.get_markdown():
            if filename not in self.skip:
                # Find the filename for the generated HTML, and convert.
                if filename == os.path.join(self.index + self.md_ext):
                    html = jala.convert(open(os.path.join(self.md_path,
                        filename)).read(), homepage=True)
                    newfilename = os.path.join(self.generate_path, self.index + self.html_ext)
                else:
                    html = jala.convert(open(os.path.join(self.md_path, filename)).read())
                    newfilename = os.path.join(self.generate_path,
                            filename[:-len(self.md_ext)], self.index + self.html_ext)
                    path = os.path.dirname(newfilename)
                    if path != '' and not os.path.exists(path):
                        os.makedirs(path)

                # Write the generated file.
                with open(newfilename, "w+") as newfile:
                    newfile.write(html)
        for filename in self.get_javascript():
            os.makedirs(os.path.join(self.generate_path, self.js_path))
            shutil.copy(os.path.join(self.dir, self.js_path, script),
                        os.path.join(self.generate_path, self.style_js, script))
        for filename in self.get_stylesheets():
            os.makedirs(os.path.join(self.generate_path, self.css_path))
            shutil.copy(os.path.join(self.dir, self.css_path, stylesheet),
                        os.path.join(self.generate_path, self.style_css, stylesheet))

    def init(self):
        pygit2.init_repository(self.project_dir)
        for path in [ self.md_path, self.generate_path ]:
            try:
                os.makedirs(path)
            except OSError:
                # Path exists, so we don't need to create it.
                pass
        self.config = config.Config(self.project_dir)
        for init_file in resources.INIT_FILES:
            if not os.path.exists(os.path.join(self.project_dir, init_file)):
                with open(os.path.join(self.project_dir, init_file), "w+") as f:
                    f.write(resources.INIT_FILES[init_file])
