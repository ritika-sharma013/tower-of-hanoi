import argparse
from tkinter import TclError

from tower_of_hanoi.ui import HanoiApp
from tower_of_hanoi.terminal_ui import run_terminal_game
from tower_of_hanoi.web_ui import run_web_game


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--terminal", action="store_true", help="use the text interface")
	parser.add_argument("--port", type=int, default=8765, help="browser game port (default: 8765)")
	args = parser.parse_args()

	if args.terminal:
		run_terminal_game()
		return

	try:
		HanoiApp().run()
	except TclError as error:
		if "display" not in str(error).lower():
			raise
		print("No graphical display found; starting browser game.")
		run_web_game(port=args.port)


if __name__ == "__main__":
	main()

