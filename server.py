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
    def __init__(ip='', port=8080):
        self.ip = ip
        self.port = port

    def run():
        httpd = HTTPServer((self.ip, self.port),
                    SundaraRequestHandler)
        httpd.serve_forever()