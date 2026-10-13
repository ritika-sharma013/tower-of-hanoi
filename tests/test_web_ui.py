import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tower_of_hanoi.web_ui import create_server


class HanoiWebTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server("127.0.0.1", 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address
        self.base_url = f"http://{host}:{port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def _post(self, path: str, payload: dict[str, object]) -> dict[str, object]:
        request = Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            return json.load(response)

    def test_page_and_initial_state_are_served(self) -> None:
        with urlopen(self.base_url) as response:
            self.assertIn(b"Tower of Hanoi", response.read())
        with urlopen(f"{self.base_url}/api/state") as response:
            state = json.load(response)
        self.assertEqual(state["pegs"]["A"], [4, 3, 2, 1])

    def test_reset_and_moves_use_game_rules(self) -> None:
        state = self._post("/api/reset", {"disk_count": 3})
        self.assertEqual(state["disk_count"], 3)

        state = self._post("/api/move", {"source": "A", "destination": "C"})
        self.assertEqual(state["move_count"], 1)

        request = Request(
            f"{self.base_url}/api/move",
            data=json.dumps({"source": "A", "destination": "C"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as context:
            urlopen(request)
        self.assertEqual(context.exception.code, 400)
        context.exception.close()


if __name__ == "__main__":
    unittest.main()