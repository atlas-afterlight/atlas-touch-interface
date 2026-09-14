import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread


LOG_FILE = Path("data/touch_events.jsonl")


def validate_touch(event):
    if event.get("type") != "touch":
        return False

    if not event.get("timestamp"):
        return False

    if not event.get("source"):
        return False

    intensity = event.get("intensity")
    if intensity is not None and not 0 <= intensity <= 1:
        return False

    confidence = event.get("confidence")
    if confidence is not None and not 0 <= confidence <= 1:
        return False

    duration_ms = event.get("duration_ms")
    if duration_ms is not None and duration_ms < 0:
        return False

    return True


def normalize_touch(event):
    return {
        "type": "touch",
        "timestamp": event["timestamp"],
        "source": event["source"],
        "gesture": event.get("gesture"),
        "intensity": event.get("intensity"),
        "duration_ms": event.get("duration_ms"),
        "location": event.get("location"),
        "confidence": event.get("confidence"),
    }


def process_touch(event):
    if not validate_touch(event):
        return {"error": "invalid_touch_event"}

    normalized = normalize_touch(event)

    with LOG_FILE.open("a", encoding="utf-8") as log:
        log.write(json.dumps(normalized) + "\n")

    print(json.dumps(normalized), flush=True)

    return normalized


class TouchHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/touch":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            event = json.loads(body)
            result = process_touch(event)
            status = 200 if "error" not in result else 400
        except (json.JSONDecodeError, TypeError, ValueError):
            result = {"error": "invalid_json"}
            status = 400

        response = json.dumps(result).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        return


def run_server():
    server = HTTPServer(("0.0.0.0", 8080), TouchHandler)
    print("Touch bridge listening on port 8080", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    Thread(target=run_server, daemon=True).start()

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        try:
            event = json.loads(line)
            process_touch(event)
        except (json.JSONDecodeError, TypeError):
            print(json.dumps({"error": "invalid_json"}), flush=True)
