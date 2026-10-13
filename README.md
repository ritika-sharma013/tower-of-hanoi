# Tower of Hanoi

A small, interactive Tower of Hanoi game built with Python's standard-library
Tkinter. Play by selecting a source peg and then a destination peg, or watch the
recursive solver demonstrate the puzzle.

## Run

```bash
python game.py
```

No third-party packages are required. Python must include Tkinter.

## Controls

- Choose a disk count from 3 to 8 and select **New game** to start or reset.
- Click a peg to select it as the source, then click another peg to move its top
	disk. Larger disks cannot be placed on smaller disks.
- Select **Next solution step** to see one move of the recursive solution.
- Select **Run solution** to watch the full solution; use **Stop** to pause it.
- The move counter tracks moves made in the current game.

The minimum number of moves needed to solve a puzzle with `n` disks is
`2^n - 1`.

## Project layout

- `game.py` starts the application.
- `tower_of_hanoi/model.py` owns puzzle state and move rules.
- `tower_of_hanoi/solver.py` generates the recursive solution.
- `tower_of_hanoi/ui.py` draws the board and handles interaction.
- `tests/` contains the model and solver tests.

## Tests

```bash
python -m unittest discover -s tests
```