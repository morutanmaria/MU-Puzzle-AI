from move import *
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

        print("\nCommands: number = apply move, u = undo, q = quit")
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

        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(moves):
                current = apply_move(current, moves[idx])
                history.append(current)
            else:
                print("Invalid move index!")
        else:
            print("Invalid command!")
