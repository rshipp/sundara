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

        # Add meta information.
        soup.head.append(BeautifulSoup().new_tag('title'))
        soup.title.string = ""
        soup.head.append(BeautifulSoup().new_tag('meta',
            charset='UTF-8'))

        # Link in Bootstrap and jQuery.
        soup.head.append(BeautifulSoup().new_tag('link', rel='stylesheet',
            href='//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css'))
        soup.body.append(BeautifulSoup().new_tag('script',
            src='//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'))
        soup.body.append(BeautifulSoup().new_tag('script',
            src='//code.jquery.com/jquery-1.11.0.min.js'))

        # Wrap everything in the appropriate tags.


        html = soup.prettify().split('\n')

        # Fix indentation for non-tag lines.
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
