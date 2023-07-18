import sys
from enum import StrEnum

from spacy import load as spacy_load

from ginza import set_split_mode

nlp = spacy_load("ja_ginza")


class SplitType(StrEnum):
    SplitTypeA = "A"
    SplitTypeB = "B"
    SplitTypeC = "C"


def split_text(text: str, split_type: SplitType):
    set_split_mode(nlp, split_type.value)
    doc = nlp(text)

    for token in doc:
        print(token)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python main.py <text>")
        sys.exit(1)

    types = SplitType.__members__.values()

    for t in types:
        print(f"---- SplitType: {t.value} ----")
        split_text(args[1], t)
        print()
