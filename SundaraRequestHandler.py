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

    def getLocalFile(file):
        """Translate the HTTP path to a local path.
           Using os.sep makes sure everything works on Windows as well
           as *nix.
        """
        file = file.replace('/', os.sep)
        # FIXME: Replace hardcoded 'www' with the `generate` path.
        return os.curdir + os.sep + 'www' + file

    def HTTPStatusFromFile(file):
        """Return an HTTP status message, one of '200 OK', '404 File
           Not Found', or '403 Forbidden', depending on whether a file
           exists and can be opened for reading.
        """
        file = getLocalFile(file)

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

    def getRequestedFile(self):
        """Parse the HTTP request and return the path to the file the
           client is looking for. If the request cannot be parsed, write
           out '400 Bad Request' to the HTTP stream.

           Requests look like

                OPTIONS *

            or

                OPTIONS /

            or
            
                GET /path HTTP/1.1

            etc.
        """
        try:
            readfile = self.rfile.read()
            file = str(readfile).split(' ')[1]
        except IndexError:
            self.wfile.write("400 Bad Request")
            file = False
        return file

    def do_OPTIONS(self):
        file = self.getRequestedFile()
        if not file:
            return

        self.wfile.write("%s\r\n" % HTTPStatusFromFile(file))
        self.wfile.write("Allow: HEAD,GET,OPTIONS\r\n")
        self.wfile.write("\r\n")

    def do_HEAD(self):
        file = self.getRequestedFile()
        if not file:
            return

        self.wfile.write("%s\r\n" % HTTPStatusFromFile(file))
        self.wfile.write("\r\n")

    def do_GET(self):
        file = self.getRequestedFile()
        if not file:
            return

        print(self.rfile.read())

        status = HTTPStatusFromFile(file)
        self.wfile.write("%s\r\n" % status)
        self.wfile.write("\r\n")

        if status == "200 OK":
            hfile = open(getLocalFile(file), 'r+')
            self.wfile.write(hfile.read())
            self.wfile.write("\r\n")

        self.wfile.close()
