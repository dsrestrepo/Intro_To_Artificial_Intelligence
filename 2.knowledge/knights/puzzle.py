from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    Or(CKnight, CKnave),
    Or(Not(CKnight), Not(CKnave)),
    # A says "I am both a knight and a knave."
    # If A says the True all values are True the A is a Knight
    Implication(AKnight, And(AKnight, AKnave)),
    # If A says a lie the afirmation is false then A is a AKnave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    Or(CKnight, CKnave),
    Or(Not(CKnight), Not(CKnave)),
    # A says "We are both knaves."
    # If A says the True all values are True the A is a Knight
    Implication(AKnight, And(AKnave, BKnave)),
    # If A says a lie the afirmation is false then A is a AKnave
    Implication(BKnave, Not(And(AKnave, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    Or(CKnight, CKnave),
    Or(Not(CKnight), Not(CKnave)),
    # A says "We are the same kind."
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # B says "We are of different kinds."
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    Or(CKnight, CKnave),
    Or(Not(CKnight), Not(CKnave)),
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # B says "A said 'I am a knave'."
    Implication(BKnight, Implication(AKnight, BKnave)),
    Implication(BKnave, Implication(AKnave, Not(BKnave))),
    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    # C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),

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
