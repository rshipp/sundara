#!/usr/bin/env python3
"""Sundara jāla
   For a beautiful web.

   jala.py
   Convert markdown to clean HTML5.
"""

# Global imports
import sys
from markdown import Markdown

# Local imports
import links


def main(args):
    md = open(args[1])
    markdown = Markdown()
    print(markdown.convert(md.read()))

if __name__ == "__main__":
    main(sys.argv)
