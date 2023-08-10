import sys

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("ja_ginza")


def has_noun(text: str, pattern_text: str) -> int:
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "NOUN", "TEXT": pattern_text}]
    matcher.add("noun-matcher", [pattern])

    doc = nlp(text)
    matched: int = 0
    for match_id, start, end in matcher(doc):
        print(f"Matched: {doc[start:end].text} at {start}:{end} ({match_id})")
        matched += 1

    return matched


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("Usage: python src/rule_based_noun_match.py <text> <pattern>")
        sys.exit(1)

    text = args[1]
    pattern = args[2]
    if has_noun(text, pattern) == 0:
        print("not matched")
