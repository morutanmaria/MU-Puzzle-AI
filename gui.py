import tkinter as tk
from tkinter import messagebox
from move import *

BG = "#f4f6f8"
CARD = "#ffffff"
PRIMARY = "#2c3e50"
ACCENT = "#3498db"
DANGER = "#e74c3c"
SUCCESS = "#27ae60"

R3_COLOR = "#f1c40f"   
R4_COLOR = "#e67e22"   

class MUPuzzleGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MU Puzzle")
        self.root.configure(bg=BG)
        self.root.geometry("760x520")

        self.current = "MI"
        self.history = [self.current]

        tk.Label(
            root,
            text="MU Puzzle",
            font=("Helvetica", 22, "bold"),
            bg=BG,
            fg=PRIMARY
        ).pack(pady=10)

        self.card = tk.Frame(
            root, bg=CARD, highlightthickness=1, highlightbackground="#ddd"
        )
        self.card.pack(padx=20, pady=10, fill="x")

        self.string_frame = tk.Frame(self.card, bg=CARD)
        self.string_frame.pack(pady=(15, 5))

        self.invariant_label = tk.Label(
            self.card,
            font=("Helvetica", 12),
            bg=CARD
        )
        self.invariant_label.pack(pady=(0, 15))

        tk.Label(
            root,
            text="Click highlighted parts of the string to apply rules",
            bg=BG,
            fg=PRIMARY,
            font=("Helvetica", 10, "italic")
        ).pack()

        buttons = tk.Frame(root, bg=BG)
        buttons.pack(pady=15)

        self.make_button(buttons, "Undo", self.undo).grid(row=0, column=0, padx=6)
        self.make_button(buttons, "Check Solvability", self.check_solvability).grid(row=0, column=1, padx=6)

        self.refresh()

    def render_clickable_string(self):
        for w in self.string_frame.winfo_children():
            w.destroy()

        s = self.current
        n = len(s)

        for i, ch in enumerate(s):
            bg = CARD

            if s[i:i+3] == "III":
                bg = R3_COLOR

            elif s[i:i+2] == "UU":
                bg = R4_COLOR

            lbl = tk.Label(
                self.string_frame,
                text=ch,
                font=("Courier New", 30, "bold"),
                bg=bg,
                fg=PRIMARY,
                padx=2
            )
            lbl.pack(side="left")
            lbl.bind("<Button-1>", lambda e, idx=i: self.on_char_click(idx))

    def update_invariant(self):
        mod = number_of_I_mod3(self.current)
        if mod == 0:
            self.invariant_label.config(
                text="I mod 3 = 0  —  Possibly solvable",
                fg=SUCCESS
            )
        else:
            self.invariant_label.config(
                text=f"I mod 3 = {mod}  —  Cannot reach MU",
                fg=DANGER
            )

    def refresh(self):
        self.render_clickable_string()
        self.update_invariant()

    def on_char_click(self, idx: int):
        s = self.current

        if s[idx:idx+3] == "III":
            self.apply_move(s[:idx] + "U" + s[idx+3:])
            return

        if s[idx:idx+2] == "UU":
            self.apply_move(s[:idx] + s[idx+2:])
            return

        if idx == len(s) - 1 and s.endswith("I"):
            self.apply_move(s + "U")
            return

        if idx == 0 and s.startswith("M"):
            x = s[1:]
            self.apply_move("M" + x + x)
            return

    def apply_move(self, new_s: str):
        self.history.append(self.current)
        self.current = new_s
        self.refresh()

    def undo(self):
        if len(self.history) > 1:
            self.current = self.history.pop()
            self.refresh()
        else:
            messagebox.showinfo("Undo", "Nothing to undo!")

    def check_solvability(self):
        if number_of_I_mod3(self.current) != 0:
            messagebox.showinfo(
                "Solvability",
                "This state CANNOT lead to MU.\n\n"
                "Reason:\n"
                "The number of I's modulo 3 is invariant."
            )
        else:
            messagebox.showinfo(
                "Solvability",
                "This state MAY lead to MU.\n"
                "(I mod 3 = 0)"
            )

    def make_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT,
            fg="white",
            activebackground="#2980b9",
            relief="flat",
            font=("Helvetica", 11),
            padx=16,
            pady=6,
            cursor="hand2"
        )

if __name__ == "__main__":
    root = tk.Tk()
    MUPuzzleGUI(root)
    root.mainloop()
