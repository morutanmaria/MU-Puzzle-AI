from typing import List, Optional, Literal

RuleName = Literal["R1", "R2", "R3", "R4"]

class Move:
    def __init__(self, rule: RuleName, description: str, result: str, index: Optional[int] = None):
        self.rule = rule
        self.description = description
        self.result = result
        self.index = index

    def __repr__(self) -> str:
        return f"Move(rule={self.rule}, description={self.description}, result={self.result}, index={self.index})"


def number_of_I_mod3(s: str) -> int:
    return s.count("I") % 3

def validate_mu_alphabet(s: str) -> None:
    if any(ch not in {"M", "I", "U"} for ch in s):
        raise ValueError("String can only be composed of {M,I,U}.")
    if not s or s[0] != "M":
        raise ValueError("String must start with M.")

def rule1_moves(s: str) -> List[Move]:
    # prima regula: daca se termina in I poti pune un U la final
    if s.endswith("I"):
        return [Move("R1", "Append U (ends with I)", s + "U")]
    return []


def rule2_moves(s: str) -> List[Move]:
    # a doua regula: MX -> MXX
    if not s.startswith("M"):
        return []
    x = s[1:]
    return [Move("R2", f"Double tail x='{x}'", "M" + x + x)]

def rule3_moves(s: str) -> List[Move]:
    #a treia: poti schimba III daca sunt consecutive cu un U
    moves: List[Move] = []
    sequence = "III"
    start = 0
    while True:
        idx = s.find(sequence, start)
        if idx == -1:
            break
        new_s = s[:idx] + "U" + s[idx + 3:]
        moves.append(Move("R3", f"Replace 'III' with 'U' at index {idx}", new_s, index=idx))
        start = idx + 1 
    return moves

def rule4_moves(s: str) -> List[Move]:
    #regula 4: poti sterge UU daca is consecutive
    moves: List[Move] = []
    sequence = "UU"
    start = 0
    while True:
        idx = s.find(sequence, start)
        if idx == -1:
            break
        new_s = s[:idx] + s[idx + 2:]
        moves.append(Move("R4", f"Delete 'UU' at index {idx}", new_s, index=idx))
        start = idx + 1
    return moves

def all_moves(s: str) -> List[Move]:
    validate_mu_alphabet(s)
    return (
        rule1_moves(s)
        + rule2_moves(s)
        + rule3_moves(s)
        + rule4_moves(s)
    )

def apply_move(s: str, move: Move) -> str:
    return move.result
