"""Sundara jāla: for a beautiful web.
File resources used by Sundara.
"""

README = """# Welcome to Sundara!

To get started, create an `index.md` inside the `md/` folder for your
site's homepage. Then run:

    git add -A
    git commit -am "Initial commit."
    sundara g

This will add `index.md` to the git index, commit it, and generate an
`index.html` in the `www/` inside your project. You can run `sundara s`
to preview the generated HTML.

Remember that Sundara uses the git index to find new markdown files, not
file globbing, so if you don't `git add` them, new files will not be
included in the generation.
"""

GITIGNORE = """# Ignore Sundara's generated HTML files.
www/
"""


