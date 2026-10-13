"""HTTP server for the browser-based Tower of Hanoi game."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import RLock
from urllib.parse import urlsplit

from tower_of_hanoi.model import HanoiGame
from tower_of_hanoi.solver import solve

PAGE_PATH = Path(__file__).with_name("static") / "index.html"


class HanoiHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True

    def __init__(self, address: tuple[str, int]) -> None:
        super().__init__(address, HanoiRequestHandler)
        self.game = HanoiGame(4)
        self.game_lock = RLock()


class HanoiRequestHandler(BaseHTTPRequestHandler):
    server: HanoiHTTPServer

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/":
            try:
                page = PAGE_PATH.read_bytes()
            except OSError:
                self.send_error(500, "Game page could not be read.")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return

        if path == "/api/state":
            with self.server.game_lock:
                self._send_json(200, self._state())
            return

        if path == "/api/solution":
            with self.server.game_lock:
                moves = list(solve(self.server.game.disk_count))
            self._send_json(200, {"moves": moves})
            return

        self.send_error(404)

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0 or length > 4096:
                raise ValueError("Invalid request size.")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Request body must be a JSON object.")
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error) or "Invalid JSON request."})
            return

        path = urlsplit(self.path).path
        try:
            with self.server.game_lock:
                if path == "/api/reset":
                    self.server.game.reset(payload.get("disk_count"))
                elif path == "/api/move":
                    self.server.game.move(payload.get("source"), payload.get("destination"))
                else:
                    self._send_json(404, {"error": "Unknown game action."})
                    return
                state = self._state()
        except (TypeError, ValueError) as error:
            self._send_json(400, {"error": str(error)})
            return

        self._send_json(200, state)

    def _state(self) -> dict[str, object]:
        game = self.server.game
        return {
            "disk_count": game.disk_count,
            "pegs": game.pegs,
            "move_count": game.move_count,
            "solved": game.is_solved,
        }

    def _send_json(self, status: int, data: object) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def create_server(host: str = "127.0.0.1", port: int = 8765) -> HanoiHTTPServer:
    """Create the web game server, exposed separately for tests."""
    return HanoiHTTPServer((host, port))


def run_web_game(port: int = 8765) -> None:
    """Serve the browser game on all interfaces for forwarded dev-container ports."""
    server = create_server("0.0.0.0", port)
    url = f"http://localhost:{server.server_address[1]}"
    print(f"Browser game ready at {url}")
    print("Press Ctrl+C to stop the game server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGame server stopped.")
    finally:
        server.server_close()