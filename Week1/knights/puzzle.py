from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
S1 = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Biconditional(AKnight, S1),
)

# Puzzle 1
# A says "We are both knaves."
S2 = And(AKnave, BKnave)
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Biconditional(AKnight, S2),
    Biconditional(AKnave, Not(S2)),
)

# Puzzle 2
# A says "We are the same kind."
S3 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
S4 = Or(And(AKnave, BKnight), And(AKnave, BKnave))
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Biconditional(AKnight, S3),
    Biconditional(BKnight, S4),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
S51 = AKnight
S52 = AKnave
# B says "A said 'I am a knave'."
S6 = Biconditional(AKnight, S52)
# B says "C is a knave."
S7 = CKnave
# C says "A is a knight."
S8 = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Or(Biconditional(AKnight, S51),Biconditional(AKnight, S52)),
    Or(Biconditional(AKnave, Not(S51)),Biconditional(AKnave, Not(S52))),
    Biconditional(BKnight, S6),
    Biconditional(BKnave, Not(S6)),
    Biconditional(BKnight, S7),
    Biconditional(BKnave, Not(S7)),
    Biconditional(CKnight, S8),
    Biconditional(CKnave, Not(S8)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
