"""Sundara jāla: for a beautiful web.

Implements the functionality for the built-in development server.
A tiny little HTTP file server, not suitable for use in production
environments.
"""

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

from sundara import config


class SundaraServer():
    def __init__(self, ip='127.0.0.1', port=8080):
        self.ip = ip
        self.port = port

    def run(self):
        print("Starting Sundara development server...")
        httpd = HTTPServer((self.ip, self.port),
                    SundaraRequestHandler)
        try:
            print("Server listening on http://%s:%s/" % (self.ip,
                        self.port))
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server shutting down...")
            httpd.shutdown()


class SundaraRequestHandler(SimpleHTTPRequestHandler):
    """Implements the functionality for the `sundara runserver` command.
    A tiny little HTTP server, not suitable for use in production
    environments.

    This is an http.server Request Handler.
    """

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
