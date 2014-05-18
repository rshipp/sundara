"""Sundara jāla
   For a beautiful web.

   config.py
   Read in configuration options from a project's Sundara config.
"""

import os

def getGeneratePath():
    return os.getcwd() + os.sep + 'www'
