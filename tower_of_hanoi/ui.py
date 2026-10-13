"""Tkinter interface for the Tower of Hanoi game."""

import tkinter as tk
from tkinter import ttk

from tower_of_hanoi.model import HanoiGame
from tower_of_hanoi.solver import Move, solve


class HanoiApp:
    """Render the puzzle and connect user actions to the game model."""

    BACKGROUND = "#f4f1e9"
    INK = "#222b2a"
    MUTED = "#64716d"
    ACCENT = "#176b5b"
    DISK_COLORS = ("#d85c41", "#e6a23c", "#4a8f83", "#4e77a5", "#86669a", "#bd7650", "#65864e", "#59626d")

    def __init__(self, root: tk.Tk | None = None) -> None:
        self.root = root or tk.Tk()
        self.root.title("Tower of Hanoi")
        self.root.geometry("960x700")
        self.root.minsize(720, 560)
        self.root.configure(background=self.BACKGROUND)

        self.game = HanoiGame(4)
        self.disk_choice = tk.IntVar(value=self.game.disk_count)
        self.move_text = tk.StringVar(value="Moves: 0")
        self.status_text = tk.StringVar(value="Select a source peg, then a destination peg.")
        self.selected_peg: str | None = None
        self.solution_moves: Iterator[Move] | None = None
        self.auto_running = False
        self.auto_after_id: str | None = None

        self._build_styles()
        self._build_layout()

    def _build_styles(self) -> None:
        style = ttk.Style(self.root)
        style.configure("App.TFrame", background=self.BACKGROUND)
        style.configure("Title.TLabel", background=self.BACKGROUND, foreground=self.INK, font=("TkDefaultFont", 24, "bold"))
        style.configure("Sub.TLabel", background=self.BACKGROUND, foreground=self.MUTED, font=("TkDefaultFont", 11))
        style.configure("Count.TLabel", background=self.BACKGROUND, foreground=self.INK, font=("TkDefaultFont", 12, "bold"))
        style.configure("Status.TLabel", background=self.BACKGROUND, foreground=self.ACCENT, font=("TkDefaultFont", 11))
        style.configure("TButton", padding=(12, 8))
        style.configure("Primary.TButton", padding=(12, 8), foreground="#ffffff", background=self.ACCENT)

    def _build_layout(self) -> None:
        shell = ttk.Frame(self.root, padding=(28, 24), style="App.TFrame")
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(2, weight=1)

        header = ttk.Frame(shell, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        ttk.Label(header, text="Tower of Hanoi", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="A classic puzzle in three pegs and a little recursion.", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        controls = ttk.Frame(shell, style="App.TFrame")
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(controls, text="DISKS", style="Count.TLabel").pack(side="left", padx=(0, 8))
        self.disk_selector = ttk.Spinbox(controls, from_=3, to=8, width=4, textvariable=self.disk_choice, state="readonly")
        self.disk_selector.pack(side="left", padx=(0, 10))
        ttk.Button(controls, text="New game", command=self.new_game).pack(side="left")
        ttk.Label(controls, textvariable=self.move_text, style="Count.TLabel").pack(side="right", padx=(12, 0))
        self.auto_button = ttk.Button(controls, text="Run solution", style="Primary.TButton", command=self.toggle_auto_solve)
        self.auto_button.pack(side="right", padx=(8, 0))
        ttk.Button(controls, text="Next solution step", command=self.next_solution_step).pack(side="right")

        board_frame = ttk.Frame(shell, style="App.TFrame")
        board_frame.grid(row=2, column=0, sticky="nsew")
        board_frame.rowconfigure(0, weight=1)
        board_frame.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(board_frame, background="#fffdf8", highlightthickness=0, height=420)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self._on_board_click)
        self.canvas.bind("<Configure>", lambda _event: self.draw_board())

        footer = ttk.Frame(shell, style="App.TFrame")
        footer.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        ttk.Label(footer, textvariable=self.status_text, style="Status.TLabel", wraplength=800).pack(anchor="w")

        self.draw_board()

    def run(self) -> None:
        self.root.mainloop()

    def new_game(self) -> None:
        self._stop_auto_solve()
        try:
            disk_count = self.disk_choice.get()
            self.game.reset(disk_count)
        except (tk.TclError, TypeError, ValueError):
            self.status_text.set("Choose a disk count from 3 to 8.")
            self.disk_choice.set(self.game.disk_count)
            return

        self.selected_peg = None
        self.solution_moves = None
        self.status_text.set("Select a source peg, then a destination peg.")
        self._update_move_count()
        self.draw_board()

    def _on_board_click(self, event: tk.Event) -> None:
        if self.auto_running:
            return
        peg_index = int(event.x / max(self.canvas.winfo_width(), 1) * 3)
        if not 0 <= peg_index < 3:
            return
        peg = HanoiGame.PEGS[peg_index]

        if self.selected_peg is None:
            if not self.game.pegs[peg]:
                self.status_text.set(f"Peg {peg} is empty. Select a peg with a disk.")
                return
            self.selected_peg = peg
            self.status_text.set(f"Peg {peg} selected. Choose a destination peg.")
            self.draw_board()
            return

        if peg == self.selected_peg:
            self.selected_peg = None
            self.status_text.set("Selection cleared. Select a source peg.")
            self.draw_board()
            return

        source = self.selected_peg
        self.selected_peg = None
        self._stop_auto_solve()
        self.solution_moves = None
        try:
            self.game.move(source, peg)
        except ValueError as error:
            self.status_text.set(str(error))
        else:
            self.status_text.set("Puzzle solved. Well done!" if self.game.is_solved else f"Moved a disk from {source} to {peg}.")
        self._update_move_count()
        self.draw_board()

    def _ensure_solution(self) -> None:
        if self.game.move_count:
            self._stop_auto_solve()
            self.game.reset()
            self.selected_peg = None
            self._update_move_count()
            self.draw_board()
            self.status_text.set("Starting the recursive demo from a fresh board.")
        if self.solution_moves is None:
            self.solution_moves = solve(self.game.disk_count)

    def next_solution_step(self) -> None:
        if self.auto_running:
            return
        self._ensure_solution()
        self._perform_solution_move()

    def toggle_auto_solve(self) -> None:
        if self.auto_running:
            self._stop_auto_solve()
            self.status_text.set("Solution paused.")
            return

        self._ensure_solution()
        self.auto_running = True
        self._set_auto_button("Stop")
        self.status_text.set("Running recursive solution...")
        self._perform_solution_move(schedule_next=True)

    def _perform_solution_move(self, schedule_next: bool = False) -> None:
        if self.solution_moves is None:
            return
        try:
            source, destination = next(self.solution_moves)
            self.game.move(source, destination)
        except StopIteration:
            self.solution_moves = None
            self._stop_auto_solve()
            self.status_text.set("Puzzle solved. Minimum move count reached.")
            return
        except ValueError as error:
            self._stop_auto_solve()
            self.solution_moves = None
            self.status_text.set(str(error))
            return

        self._update_move_count()
        self.draw_board()
        if self.game.is_solved:
            self.solution_moves = None
            self._stop_auto_solve()
            self.status_text.set("Puzzle solved. Minimum move count reached.")
        elif schedule_next and self.auto_running:
            self.auto_after_id = self.root.after(420, lambda: self._perform_solution_move(schedule_next=True))

    def _stop_auto_solve(self) -> None:
        if self.auto_after_id is not None:
            self.root.after_cancel(self.auto_after_id)
            self.auto_after_id = None
        self.auto_running = False
        self._set_auto_button("Run solution")

    def _set_auto_button(self, label: str) -> None:
        if hasattr(self, "auto_button"):
            self.auto_button.configure(text=label)

    def _update_move_count(self) -> None:
        self.move_text.set(f"Moves: {self.game.move_count}")

    def draw_board(self) -> None:
        if not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 600)
        height = max(self.canvas.winfo_height(), 360)
        base_y = height - 58
        peg_top = 64
        peg_centers = [width * (index + 0.5) / 3 for index in range(3)]
        base_left, base_right = width * 0.08, width * 0.92

        self.canvas.create_rectangle(base_left, base_y, base_right, base_y + 12, fill="#64716d", outline="")
        for index, peg in enumerate(HanoiGame.PEGS):
            center = peg_centers[index]
            peg_color = self.ACCENT if peg == self.selected_peg else "#a5ada6"
            self.canvas.create_rectangle(center - 5, peg_top, center + 5, base_y, fill=peg_color, outline="")
            self.canvas.create_text(center, base_y + 32, text=peg, fill=self.INK, font=("TkDefaultFont", 12, "bold"))
            for level, disk in enumerate(self.game.pegs[peg]):
                disk_height = 25
                disk_width = 72 + (disk - 1) * (150 / max(self.game.disk_count - 1, 1))
                y_bottom = base_y - level * (disk_height + 3)
                x_left, x_right = center - disk_width / 2, center + disk_width / 2
                color = self.DISK_COLORS[(disk - 1) % len(self.DISK_COLORS)]
                self.canvas.create_rectangle(x_left, y_bottom - disk_height, x_right, y_bottom, fill=color, outline="")
                self.canvas.create_text(center, y_bottom - disk_height / 2, text=str(disk), fill="#fffdf8", font=("TkDefaultFont", 10, "bold"))

        if self.selected_peg is not None:
            center = peg_centers[HanoiGame.PEGS.index(self.selected_peg)]
            self.canvas.create_oval(center - 7, peg_top - 20, center + 7, peg_top - 6, fill=self.ACCENT, outline="")