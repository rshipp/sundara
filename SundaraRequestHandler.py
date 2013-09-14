#!/usr/bin/env python3
"""Sundara jāla
   For a beautiful web.

   SundaraRequestHandler.py
   Implements the functionality for the `sundara runserver` command.
   A tiny little HTTP server, not suitable for use in production
   environments.

   This is an http.server Request Handler.
"""

import os
from urllib.parse import unquote
from http.server import SimpleHTTPRequestHandler

import config

class SundaraRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        """This function overwrites that in 
           http.server.SimpleHTTPRequestHandler and modifies it to
           serve files from the Sundara `generate` path instead of the
           cwd.
        """
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = os.path.normpath(unquote(path))
        words = path.split(os.sep)
        words = filter(None, words)
        path = config.getGeneratePath()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
