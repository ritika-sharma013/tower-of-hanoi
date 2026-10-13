import io
import unittest

from tower_of_hanoi.terminal_ui import run_terminal_game


class TerminalGameTests(unittest.TestCase):
    def test_solver_command_completes_puzzle(self) -> None:
        commands = iter(("3", "solve"))
        output = io.StringIO()

        run_terminal_game(lambda _prompt: next(commands), output)

        self.assertIn("Solved in 7 moves.", output.getvalue())
        self.assertIn("C: [3, 2, 1]", output.getvalue())

    def test_illegal_move_is_reported_and_does_not_end_game(self) -> None:
        commands = iter(("3", "A C", "A C", "q"))
        output = io.StringIO()

        run_terminal_game(lambda _prompt: next(commands), output)

        self.assertIn("A larger disk cannot be placed on a smaller disk.", output.getvalue())
        self.assertIn("Game ended.", output.getvalue())


if __name__ == "__main__":
    unittest.main()