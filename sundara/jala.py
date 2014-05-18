"""Sundara jāla: for a beautiful web.

Convert markdown to clean HTML5.
"""

import sys
import re
from markdown import Markdown
from bs4 import BeautifulSoup

DOCTYPE="<!DOCTYPE html>\n"

class Jala():
    """Convert Markdown to clean, properly formatted HTML5."""
    def __init__(self):
        pass

    def convert(self, md):
        markdown = Markdown(output_format="html5")
        soup = BeautifulSoup(DOCTYPE + markdown.convert(md), "html5lib")
        html = soup.prettify().split('\n')

        # Fix indentation for non-tag lines
        for index, line in enumerate(html):
            if index > 0 and re.match("\s*[^<\s]", line) and re.match("\s+[^<\s]", html[index - 1]):
                # if line isn't a tag and previous line is indented and not a tag
                html[index] = re.match("\s*", html[index - 1]).group() + line

        return '\n'.join(html)


def main(args):
    md = open(args[1])
    print(Jala().convert(md.read()))

if __name__ == "__main__":
    main(sys.argv)
