"""Small read-only HTTP API for the mobile dashboard."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

try:
    from .event_store import read_alerts, read_events
    from .summary_engine import build_summary
except ImportError:
    from event_store import read_alerts, read_events
    from summary_engine import build_summary

MOBILE_PAGE = Path(__file__).resolve().parent.parent / "mobile" / "dashboard.html"


class DashboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_dashboard(self) -> None:
        body = MOBILE_PAGE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route == "/":
            self._send_dashboard()
        elif route == "/api/events":
            self._send_json(read_events())
        elif route == "/api/alerts":
            self._send_json(read_alerts())
        elif route == "/api/summary":
            self._send_json(build_summary(read_events()))
        elif route == "/health":
            self._send_json({"status": "ok"})
        else:
            self._send_json({"error": "Not found"}, 404)

    def log_message(self, format_string: str, *args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Quantum Phoenix mobile dashboard API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Dashboard API listening at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard API")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
