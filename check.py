import subprocess
import tempfile
import os
from tkinter import messagebox

MACE4_PATH = os.path.join("tools", "mace4")

def check_solvability():
    mace4_input = r"""formulas(assumptions).

Reachable(mi).

z0 != z1.
z0 != z2.
z1 != z2.

inv(mi) = z1.
inv(mu) = z0.

all x (inv(r1(x)) = inv(x)).
all x (inv(r3(x)) = inv(x)).
all x (inv(r4(x)) = inv(x)).

mul2(z0) = z0.
mul2(z1) = z2.
mul2(z2) = z1.
all x (inv(r2(x)) = mul2(inv(x))).

all x (Reachable(x) -> Reachable(r1(x))).
all x (Reachable(x) -> Reachable(r2(x))).
all x (Reachable(x) -> Reachable(r3(x))).
all x (Reachable(x) -> Reachable(r4(x))).

all x (Reachable(x) -> inv(x) != z0).

end_of_list.

formulas(goals).
Reachable(mu).
end_of_list.
"""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".in") as f:
        f.write(mace4_input)
        mace4_file = f.name

    try:
        if not os.path.exists(MACE4_PATH):
            messagebox.showerror("Solvability", f"Mace4 not found at:\n{MACE4_PATH}")
            return
        try:
            result = subprocess.run(
                [MACE4_PATH, "-n", "3", "-f", mace4_file],
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            messagebox.showwarning("Solvability", "Mace4 timeout (5s).")
            return

        output = (result.stdout or "") + "\n" + (result.stderr or "")
        low = output.lower()

        if ("unsatisfiability detected" in low) or ("0 models" in low) or ("no models" in low):
            messagebox.showinfo(
                "Solvability",
                "This state CANNOT lead to MU.\n\n"
                "Reason:\n"
                "Mace4 reports UNSAT under a Mod-3 invariant."
            )
        else:
            messagebox.showinfo(
                "Solvability",
                "Mace4 did not report UNSAT/0-models.\n\n"
                "Check console output for details."
            )
            print("\n=== Mace4 Output ===")
            print(output)
    except FileNotFoundError:
        messagebox.showerror("Solvability", "Mace4 not found. Please install Mace4.")