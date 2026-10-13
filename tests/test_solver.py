import unittest

from tower_of_hanoi.model import HanoiGame
from tower_of_hanoi.solver import solve


class HanoiSolverTests(unittest.TestCase):
    def test_solver_completes_in_minimum_number_of_moves(self) -> None:
        for disk_count in range(1, 7):
            with self.subTest(disk_count=disk_count):
                game = HanoiGame(disk_count)
                moves = list(solve(disk_count))

                for source, destination in moves:
                    game.move(source, destination)

                self.assertTrue(game.is_solved)
                self.assertEqual(len(moves), 2**disk_count - 1)
                self.assertEqual(game.move_count, 2**disk_count - 1)

    def test_solver_rejects_invalid_peg_selection(self) -> None:
        with self.assertRaises(ValueError):
            solve(3, source="A", destination="A", auxiliary="C")

    def test_solver_handles_custom_peg_order(self) -> None:
        game = HanoiGame(4)
        game.pegs = {"A": [], "B": [4, 3, 2, 1], "C": []}
        moves = list(solve(4, source="B", destination="A", auxiliary="C"))

        for source, destination in moves:
            game.move(source, destination)

        self.assertEqual(game.pegs["A"], [4, 3, 2, 1])
        self.assertEqual(len(moves), 15)


if __name__ == "__main__":
    unittest.main()