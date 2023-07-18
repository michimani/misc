import sys

from tabulate import tabulate

from utils.nlp import SplitMode, split_with_mode


def split_text(text: str, split_mode: SplitMode):
    doc = split_with_mode(text, split_mode)

    table = []
    for token in doc:
        table.append([token.text, token.tag_, token.pos_])

    print(tabulate(table, headers=["text", "tag", "pos"]))


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
