"""Sundara jāla: for a beautiful web.

Implements the functionality for the `sundara server` command.
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
