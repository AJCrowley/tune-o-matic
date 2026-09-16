#!/usr/bin/python3
"""tune-o-matic origin server: plain file serving with Cache-Control: no-cache on
everything, so manual or agent edits always propagate on the next hard refresh
through the Cloudflare tunnel. tuneomatic.service runs this."""
import http.server, functools, os

ROOT = "/home/crowley/projects/tuneomatic"

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()

handler = functools.partial(NoCacheHandler, directory=ROOT)
if __name__ == "__main__":
    http.server.HTTPServer(("0.0.0.0", 8088), handler).serve_forever()
