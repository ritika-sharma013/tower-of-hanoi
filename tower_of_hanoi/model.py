"""Puzzle state and legal move rules for Tower of Hanoi."""


class HanoiGame:
    """Maintain the state of a three-peg Tower of Hanoi puzzle."""

    PEGS = ("A", "B", "C")

    def __init__(self, disk_count: int = 3) -> None:
        self._validate_disk_count(disk_count)
        self.disk_count = disk_count
        self.reset()

    @staticmethod
    def _validate_disk_count(disk_count: int) -> None:
        if isinstance(disk_count, bool) or not isinstance(disk_count, int):
            raise TypeError("Disk count must be an integer.")
        if disk_count < 1:
            raise ValueError("Disk count must be at least 1.")

    def reset(self, disk_count: int | None = None) -> None:
        """Restore the puzzle to its starting state, optionally changing size."""
        if disk_count is not None:
            self._validate_disk_count(disk_count)
            self.disk_count = disk_count

        self.pegs = {
            "A": list(range(self.disk_count, 0, -1)),
            "B": [],
            "C": [],
        }
        self.move_count = 0

    def move(self, source: str, destination: str) -> None:
        """Move the top disk, raising ValueError when the move is illegal."""
        if source not in self.PEGS or destination not in self.PEGS:
            raise ValueError("Choose one of the pegs A, B, or C.")
        if source == destination:
            raise ValueError("Choose two different pegs.")
        if not self.pegs[source]:
            raise ValueError(f"Peg {source} has no disk to move.")

        disk = self.pegs[source][-1]
        if self.pegs[destination] and self.pegs[destination][-1] < disk:
            raise ValueError("A larger disk cannot be placed on a smaller disk.")

        self.pegs[source].pop()
        self.pegs[destination].append(disk)
        self.move_count += 1

    @property
    def is_solved(self) -> bool:
        """Whether every disk has been moved to the final peg."""
        return len(self.pegs["C"]) == self.disk_count