"""Sundara jāla: for a beautiful web.
"""

import os
from pygit2 import Repository

from sundara.jala import Jala

class Sundara():
    def __init__(self, dir):
        self.dir = dir
        self.md_dir = os.path.join(self.dir, 'md')
        self.generate_dir = os.path.join(self.dir, 'www')

    def get_files(self):
        repo = Repository(self.dir)
        return [ f.path[3:] for f in repo.index if (f.path.endswith('.md')
                and f.path.startswith(self.md_dir + os.path.sep)) ]

    def generate(self):
        jala = Jala()
        for file in self.get_files():
            html = jala.convert(open(file).read())
            if file == os.path.join(self.md_dir, 'index.md'):
                newfilename = os.path.join(self.generate_dir, 'index.html')
            else:
                newfilename = os.path.join(self.generate_dir, file[3:-3],
                        'index.html')
                dir = os.path.dirname(newfilename)
                if dir != '' and not os.path.exists(dir):
                    os.makedirs(dir)
            with open(newfilename, "w+") as newfile:
                newfile.write(html)

    def init(self):
        pygit2.init_repository(self.dir)
        os.makedirs(self.md_dir)
        os.makedirs(self.generate_dir)
