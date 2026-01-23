import tkinter as tk
from tkinter import messagebox
from move import *

BG = "#f4f6f8"
CARD = "#ffffff"
PRIMARY = "#2c3e50"
ACCENT = "#3498db"
DANGER = "#e74c3c"
SUCCESS = "#27ae60"

class MUPuzzleGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MU Puzzle")
        self.root.configure(bg=BG)
        self.root.geometry("720x520")

        self.current = "MI"
        self.history = [self.current]

        tk.Label(
            root,
            text="MU Puzzle",
            font=("Helvetica", 22, "bold"),
            bg=BG,
            fg=PRIMARY
        ).pack(pady=10)

  
        self.card = tk.Frame(root, bg=CARD, bd=0, highlightthickness=1,
                             highlightbackground="#ddd")
        self.card.pack(padx=20, pady=10, fill="x")

        self.string_label = tk.Label(
            self.card,
            text=self.current,
            font=("Courier New", 30, "bold"),
            bg=CARD,
            fg=PRIMARY
        )
        self.string_label.pack(pady=(15, 5))

        self.invariant_label = tk.Label(
            self.card,
            text="",
            font=("Helvetica", 12),
            bg=CARD
        )
        self.invariant_label.pack(pady=(0, 15))

        moves_container = tk.Frame(root, bg=BG)
        moves_container.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(
            moves_container,
            text="Available Moves",
            font=("Helvetica", 14, "bold"),
            bg=BG,
            fg=PRIMARY
        ).pack(anchor="w", pady=(0, 5))

        self.moves_listbox = tk.Listbox(
            moves_container,
            height=8,
            font=("Courier New", 11),
            selectbackground=ACCENT,
            activestyle="none"
        )
        self.moves_listbox.pack(fill="both", expand=True)
        self.moves_listbox.bind("<Double-Button-1>", self.apply_selected_move)

        buttons = tk.Frame(root, bg=BG)
        buttons.pack(pady=15)

        self.make_button(buttons, "Apply Move", self.apply_selected_move).grid(row=0, column=0, padx=5)
        self.make_button(buttons, "Undo", self.undo).grid(row=0, column=1, padx=5)
        self.make_button(buttons, "Check Solvability", self.check_solvability).grid(row=0, column=2, padx=5)

        self.refresh_moves()

    def make_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT,
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            font=("Helvetica", 11),
            padx=15,
            pady=6,
            cursor="hand2"
        )

    def invariant_text(self):
        mod = number_of_I_mod3(self.current)
        color = SUCCESS if mod == 0 else DANGER
        text = f"I mod 3 = {mod}  —  {'Possibly solvable' if mod == 0 else 'Cannot reach MU'}"
        self.invariant_label.config(text=text, fg=color)

    def refresh_moves(self):
        self.string_label.config(text=self.current)
        self.invariant_text()

        self.moves_listbox.delete(0, tk.END)
        self.moves = all_moves(self.current)

        if not self.moves:
            self.moves_listbox.insert(tk.END, "No moves available.")
        else:
            for i, move in enumerate(self.moves):
                self.moves_listbox.insert(
                    tk.END,
                    f"{i}) {move.rule}: {move.description} → {move.result}"
                )

    def apply_selected_move(self, event=None):
        sel = self.moves_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self.moves):
            return

        self.current = apply_move(self.current, self.moves[idx])
        self.history.append(self.current)
        self.refresh_moves()

    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.current = self.history[-1]
            self.refresh_moves()
        else:
            messagebox.showinfo("Undo", "Nothing to undo!")

    def check_solvability(self):
        if number_of_I_mod3(self.current) == 0:
            msg = "This state MAY lead to MU.\n(I mod 3 = 0)"
        else:
            msg = (
                "This state CANNOT lead to MU.\n\n"
                "Invariant:\n"
                "The number of I's is never divisible by 3\n"
                "starting from MI."
            )
        messagebox.showinfo("Solvability", msg)


if __name__ == "__main__":
    root = tk.Tk()
    MUPuzzleGUI(root)
    root.mainloop()
