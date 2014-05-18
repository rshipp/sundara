"""Sundara jāla: for a beautiful web.
"""

import os
import pygit2

from sundara.jala import Jala
from sundara import resources
from sundara import config

class Sundara():
    def __init__(self, dir):
        self.dir = dir
        self.index = 'index'
        self.html_ext = '.html'
        self.md_ext = '.md'

        conf_file = os.path.join(self.dir, config.PROJECT_CONF)
        if os.path.exists(conf_file):
            self.config = config.Config(conf_file)
            self.md_dir = self.config.get('sundara', 'md')
            self.generate_path = os.path.join(self.dir,
                    self.config.get('sundara', 'generate'))
        else:
            self.md_dir = 'md/'
            self.generate_path = os.path.join(self.dir, 'www/')

        self.md_path = os.path.join(self.dir, self.md_dir)

    def get_files(self):
        repo = pygit2.Repository(self.dir)
        return [ f.path[len(self.md_dir):] for f in repo.index if (f.path.endswith(self.md_ext)
                and f.path.startswith(self.md_dir)) ]

    def generate(self):
        # Clean up the generation directory.
        shutil.rmtree(self.generate_path)
        os.makedirs(self.generate_path)

        jala = Jala()
        for file in self.get_files():
            html = jala.convert(open(os.path.join(self.md_path, file)).read())

            # Find the filename for the generated html.
            if file == os.path.join(self.index + self.md_ext):
                newfilename = os.path.join(self.generate_path, self.index + self.html_ext)
            else:
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
        os.makedirs(self.md_path)
        os.makedirs(self.generate_path)
        self.config = config.Config(self.dir)
        for file in resources.INIT_FILES:
            with open(os.path.join(self.dir, file), "w+") as f:
                f.write(resources.INIT_FILES[file])
