# Tower of Hanoi

A small, interactive Tower of Hanoi game built with Python's standard-library
Tkinter. Play by selecting a source peg and then a destination peg, or watch the
recursive solver demonstrate the puzzle.

## Run

```bash
python game.py
```

No third-party packages are required. Python must include Tkinter. If no
graphical display is available, the game serves its graphical browser version
at `http://localhost:8765` instead. Use `--port` to choose another port.

## Controls

- Choose a disk count from 3 to 8 and select **New game** to start or reset.
- Click a peg to select it as the source, then click another peg to move its top
	disk. Larger disks cannot be placed on smaller disks.
- Select **Next solution step** to see one move of the iterative solution.
- Select **Run solution** to watch the full solution; use **Stop** to pause it.
- The move counter tracks moves made in the current game.

For a text-only session, run `python game.py --terminal`. Enter two peg names
such as `A C` to move a disk, `solve` to watch the recursive solution, or `q`
to quit.

The minimum number of moves needed to solve a puzzle with `n` disks is
`2^n - 1`. The solution is generated iteratively, without recursion.

## Project layout

- `game.py` starts the application.
- `tower_of_hanoi/model.py` owns puzzle state and move rules.
- `tower_of_hanoi/solver.py` generates the recursive solution.
- `tower_of_hanoi/ui.py` draws the board and handles interaction.
- `tower_of_hanoi/web_ui.py` serves the browser version and game API.
- `tests/` contains the model and solver tests.

## Tests

```bash
python -m unittest discover -s tests
```