import sys

from utils.nlp import SplitMode, split_with_mode


def split_text(text: str, split_mode: SplitMode):
    doc = split_with_mode(text, split_mode)

    print("text\ttag\tpos\tlemma")
    for token in doc:
        print(f"{token.text}\t{token.tag_}\t{token.pos_}\t{token.lemma_}")


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python main.py <text>")
        sys.exit(1)

    types = SplitMode.__members__.values()

    for t in types:
        print(f"---- SplitMode: {t.value} ----")
        split_text(args[1], t)
        print()
