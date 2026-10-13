import unittest

from tower_of_hanoi.model import HanoiGame


class HanoiGa5meTests(unittest.TestCase):
    def test_starts_with_all_disks_on_first_peg(self) -> None:
        game = HanoiGame(3)
        self.assertEqual(game.pegs, {"A": [3, 2, 1], "B": [], "C": []})
        self.assertEqual(game.move_count, 0)

    def test_legal_move_updates_state_and_count(self) -> None:
        game = HanoiGame(2)
        game.move("A", "B")
        self.assertEqual(game.pegs, {"A": [2], "B": [1], "C": []})
        self.assertEqual(game.move_count, 1)

    def test_illegal_moves_do_not_change_state(self) -> None:
        game = HanoiGame(2)
        game.move("A", "B")
        before = {peg: disks.copy() for peg, disks in game.pegs.items()}

        with self.assertRaises(ValueError):
            game.move("A", "B")
        with self.assertRaises(ValueError):
            game.move("C", "A")
        with self.assertRaises(ValueError):
            game.move("B", "B")

        self.assertEqual(game.pegs, before)
        self.assertEqual(game.move_count, 1)

    def test_reset_can_change_disk_count_and_clears_solved_state(self) -> None:
        game = HanoiGame(1)
        game.move("A", "C")
        self.assertTrue(game.is_solved)

        game.reset(3)

        self.assertFalse(game.is_solved)
        self.assertEqual(game.pegs["A"], [3, 2, 1])
        self.assertEqual(game.move_count, 0)


if __name__ == "__main__":
    unittest.main()