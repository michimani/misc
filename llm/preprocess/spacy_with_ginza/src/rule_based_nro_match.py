import sys
from typing import Any, Dict

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("ja_ginza")


def extract_nro(text: str):
    matcher = Matcher(nlp.vocab)
    patterns: list[list[Dict[str, Any]]] = [
        [
            {"DEP": "nsubj"},
            {"OP": "*"},
            {"DEP": "acl"},
            {"DEP": "obj"},
            {"OP": "*"},
            {"DEP": "ROOT"},
        ],
        [
            {"DEP": "nsubj"},
            {"OP": "*"},
            {"DEP": "amod"},
            {"DEP": "obj"},
            {"OP": "*"},
            {"DEP": "ROOT"},
        ],
    ]
    matcher.add("noun-matcher", patterns)

    doc = nlp(text)
    matched: int = 0
    for span in doc.sents:
        for match_id, start, end in matcher(span):
            print(f"Matched: {span[start:end].text} at {start}:{end} ({match_id})")
            for token in span:
                if token.dep_ == "obj":
                    print(
                        f"\t {span[start].lemma_} : {span[end-1].lemma_}: {span[start+2].lemma_} : {token.text}"
                    )
            matched += 1

    return matched


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python src/rule_based_nro_match.py <text>")
        sys.exit(1)

    text = args[1]
    if extract_nro(text) == 0:
        print("not matched")
