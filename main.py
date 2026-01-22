import subprocess
import tempfile
from move import *

def check_solvability():
    mace4_input = """
    formulas(assumptions).
      # MU puzzle: number of I's mod 3 is never 0 in any reachable string
      Reachable(MI).
      all x (Reachable(x) -> number_of_I_mod3(x) !=0).
    end_of_list.  

    formulas(goals).
      Reachable(MU).
    end_of_list.
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".in") as f:
        f.write(mace4_input)
        mace4_file = f.name

    try:
        # Run Mace4
        result = subprocess.run(["mace4", "-f", mace4_file], capture_output=True, text=True)
        output = result.stdout + "\n" + result.stderr
        if "No" in output or "0 models found" in output:
            print("MU is unreachable. Mod-3 invariant prevents it!")
        else:
            print("Mace4 found a countermodel (unexpected).")
        print("\n=== Mace4 Output ===")
        print(output)
    except FileNotFoundError:
        print("Mace4 not found. Please install Mace4 to use solvability check.")


if __name__ == "__main__":
    current = "MI"
    history = [current]

    while True:
        print("Current:", current)
        print("I mod 3 =", number_of_I_mod3(current))

        moves = all_moves(current)

        if not moves:
            print("No moves available.")
            break

        for i, m in enumerate(moves):
            print(f"{i}) {m.rule} - {m.description} => {m.result}")

        print("\nCommands: number = apply move, u = undo, q = quit, s = check solvability")
        choice = input("Choose: ").strip().lower()

        if choice == "q":
            print("Bye!")
            break

        if choice == "u":
            if len(history) > 1:
                history.pop()
                current = history[-1]
            else:
                print("Nothing to undo!")
            continue

        if choice == "s":
            check_solvability()
            continue

        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(moves):
                current = apply_move(current, moves[idx])
                history.append(current)
            else:
                print("Invalid move index!")
        else:
            print("Invalid command!")
