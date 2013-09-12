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
from http.server import BaseHTTPRequestHandler

class SundaraRequestHandler(BaseHTTPRequestHandler):

    def getLocalFile(self):
        """Translate the HTTP path to a local path.
           Using os.sep makes sure everything works on Windows as well
           as *nix.
        """
        file = self.path
        file = file.replace('/', os.sep)
        # FIXME: Replace hardcoded 'www' with the `generate` path.
        return os.curdir + os.sep + 'www' + file

    def HTTPStatusFromFile(self):
        """Return an HTTP status message, one of '200 OK', '404 File
           Not Found', or '403 Forbidden', depending on whether a file
           exists and can be opened for reading.
        """
        file = self.getLocalFile()

        if os.path.isdir(file):
            file = file + os.sep + "index.html"

        try:
            f = open(file, "r+")
            f.close()
        except IOError:
            return "404 File Not Found"
        except PermissionError:
            return "403 Forbidden"
        return "200 OK"

    def do_OPTIONS(self):
        self.wfile.write("%s %s\r\n" % (self.request_version,
                    self.HTTPStatusFromFile()))
        self.wfile.write("Allow: HEAD,GET,OPTIONS\r\n")
        self.wfile.write("\r\n")

    def do_HEAD(self):
        self.wfile.write("%s %s\r\n" % (self.request_version,
                    self.HTTPStatusFromFile()))
        self.wfile.write("\r\n")

    def do_GET(self):
        status = self.HTTPStatusFromFile()
        self.wfile.write("%s %s\r\n" % (self.request_version, status))
        self.wfile.write("\r\n")

        if status == "200 OK":
            hfile = open(self.getLocalFile(), 'r+')
            self.wfile.write(hfile.read())
            self.wfile.write("\r\n")
