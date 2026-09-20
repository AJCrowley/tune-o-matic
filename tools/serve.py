#!/usr/bin/python3
"""tune-o-matic origin server: plain file serving with Cache-Control: no-cache on
everything, so manual or agent edits always propagate on the next hard refresh
through the Cloudflare tunnel. tuneomatic.service runs this.

2026-09-20: privacy-friendly access log (Kris: track site loads without Google
Analytics, keeping the readme's no-analytics promise). Every request appends a
Common-Log-Format-style line to tuneomatic/.traffic/access-YYYY-MM-DD.log:
path, status, bytes, UA, timestamp. No IPs (cloudflared strips client IPs
before the origin sees the request), no cookies, no identifiers. The log
stays on the Pi and is gitignored."""
import http.server, functools, os
from datetime import datetime, timezone

ROOT = "/home/crowley/projects/tuneomatic"
LOG_DIR = os.path.join(ROOT, ".traffic")
os.makedirs(LOG_DIR, exist_ok=True)

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Common-Log-Format-ish line, minus IP (origin only ever sees 127.0.0.1).
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        stamp = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S +0000")
        line = (f'- - - [{stamp}] '
                f'{format % args} "{self.headers.get("User-Agent", "-")}"\n')
        path = os.path.join(LOG_DIR, f"access-{day}.log")
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line)
        except OSError:
            pass  # never let logging break serving
        super().log_message(format, *args)  # keep the systemd journal line too

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()

handler = functools.partial(NoCacheHandler, directory=ROOT)
if __name__ == "__main__":
    http.server.HTTPServer(("0.0.0.0", 8088), handler).serve_forever()
