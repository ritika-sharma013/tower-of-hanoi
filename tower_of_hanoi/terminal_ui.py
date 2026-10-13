"""Keyboard interface for playing Tower of Hanoi without a display."""

import sys
from collections.abc import Callable
from typing import TextIO

from tower_of_hanoi.model import HanoiGame
from tower_of_hanoi.solver import solve


def run_terminal_game(
    input_fn: Callable[[str], str] | None = None,
    output: TextIO | None = None,
) -> None:
    """Play the puzzle in a terminal when a graphical display is unavailable."""
    read = input_fn or input
    write_to = output or sys.stdout
    print("\nTower of Hanoi | Terminal Mode", file=write_to)

    while True:
        try:
            disk_text = read("Choose disk count (3-8) [3]: ").strip()
        except EOFError:
            print("Input closed. Exiting.", file=write_to)
            return
        if not disk_text:
            disk_count = 3
            break
        try:
            disk_count = int(disk_text)
        except ValueError:
            print("Enter a whole number from 3 to 8.", file=write_to)
            continue
        if 3 <= disk_count <= 8:
            break
        print("Disk count must be between 3 and 8.", file=write_to)

    game = HanoiGame(disk_count)
    while not game.is_solved:
        print(f"\nMoves: {game.move_count}", file=write_to)
        for peg in HanoiGame.PEGS:
            print(f"  {peg}: {game.pegs[peg]} (bottom to top)", file=write_to)

        try:
            command = read("Move (A C), solve, or q: ").strip().upper()
        except EOFError:
            print("Input closed. Exiting.", file=write_to)
            return

        if command in {"Q", "QUIT", "EXIT"}:
            print("Game ended.", file=write_to)
            return
        if command == "SOLVE":
            for source, destination in solve(game.disk_count):
                game.move(source, destination)
            break

        pegs = command.split()
        if len(pegs) != 2:
            print("Enter a source and destination, such as A C.", file=write_to)
            continue
        try:
            game.move(pegs[0], pegs[1])
        except ValueError as error:
            print(error, file=write_to)

    print(f"\nSolved in {game.move_count} moves.", file=write_to)
    print(f"  C: {game.pegs['C']} (bottom to top)", file=write_to)