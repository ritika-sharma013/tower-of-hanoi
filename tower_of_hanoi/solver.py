"""Iterative solution generator for Tower of Hanoi."""

from collections.abc import Iterator

Move = tuple[str, str]
_PEGS = {"A", "B", "C"}


def solve(
    disk_count: int,
    source: str = "A",
    destination: str = "C",
    auxiliary: str = "B",
) -> Iterator[Move]:
    """Yield the minimum sequence of moves without recursion."""
    if isinstance(disk_count, bool) or not isinstance(disk_count, int):
        raise TypeError("Disk count must be an integer.")
    if disk_count < 1:
        raise ValueError("Disk count must be at least 1.")
    if {source, destination, auxiliary} != _PEGS:
        raise ValueError("Source, destination, and auxiliary must be A, B, and C.")

    def generate_moves() -> Iterator[Move]:
        pegs = {
            source: list(range(disk_count, 0, -1)),
            destination: [],
            auxiliary: [],
        }
        cycle = (source, auxiliary, destination) if disk_count % 2 == 0 else (source, destination, auxiliary)
        smallest_peg = source

        for move_number in range(1, 2**disk_count):
            if move_number % 2 == 1:
                cycle_index = cycle.index(smallest_peg)
                next_peg = cycle[(cycle_index + 1) % len(cycle)]
                pegs[smallest_peg].pop()
                pegs[next_peg].append(1)
                yield smallest_peg, next_peg
                smallest_peg = next_peg
                continue

            first, second = (peg for peg in (source, destination, auxiliary) if peg != smallest_peg)
            if pegs[first] and (not pegs[second] or pegs[first][-1] < pegs[second][-1]):
                start, end = first, second
            else:
                start, end = second, first
            disk = pegs[start].pop()
            pegs[end].append(disk)
            yield start, end

    return generate_moves()