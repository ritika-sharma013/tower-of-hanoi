"""Recursive solution generator for Tower of Hanoi."""

from collections.abc import Iterator

Move = tuple[str, str]
_PEGS = {"A", "B", "C"}


def solve(
    disk_count: int,
    source: str = "A",
    destination: str = "C",
    auxiliary: str = "B",
) -> Iterator[Move]:
    """Yield the minimum sequence of moves for a Tower of Hanoi puzzle."""
    if isinstance(disk_count, bool) or not isinstance(disk_count, int):
        raise TypeError("Disk count must be an integer.")
    if disk_count < 1:
        raise ValueError("Disk count must be at least 1.")
    if {source, destination, auxiliary} != _PEGS:
        raise ValueError("Source, destination, and auxiliary must be A, B, and C.")

    def move_stack(count: int, start: str, end: str, spare: str) -> Iterator[Move]:
        if count == 1:
            yield start, end
            return
        yield from move_stack(count - 1, start, spare, end)
        yield start, end
        yield from move_stack(count - 1, spare, end, start)

    return move_stack(disk_count, source, destination, auxiliary)