"""Sundara jāla: for a beautiful web.

Read in configuration options from a project's Sundara config.
"""

import os

def getGeneratePath():
    return os.path.join(os.getcwd(), 'www')
