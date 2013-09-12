#!/usr/bin/env python3
"""Sundara jāla
   For a beautiful web.

   server.py
   Implements the functionality for the `sundara runserver` command.
   A tiny little HTTP server, not suitable for use in production
   environments.
"""

from http.server import HTTPServer
from SundaraRequestHandler import SundaraRequestHandler

class SundaraServer:
    def __init__(self, ip='127.0.0.1', port=8080):
        self.ip = ip
        self.port = port

    def run(self):
        httpd = HTTPServer((self.ip, self.port),
                    SundaraRequestHandler)
        httpd.serve_forever()
