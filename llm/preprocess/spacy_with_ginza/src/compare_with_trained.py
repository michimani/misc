import sys
from typing import Optional

from spacy import blank as spacy_blank
from spacy import load as spacy_load
from spacy.language import Language

from utils.nlp import simple_tokenize


def ner(text: str, nlp: Optional[Language]):
    doc = simple_tokenize(text, nlp)
    print("text\tlabel\tstart\tend")
    for entity in doc.ents:
        print(f"{entity.text}\t{entity.label_}\t{entity.start_char}\t{entity.end_char}")


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print(
            "Usage: python src/compare_with_trained.py <text> <path to trained model>"
        )
        sys.exit(1)

    text = args[1]
    blank_nlp = spacy_blank("ja")
    trained_nlp = spacy_load(args[2])

    print("--- default nlp ('blank(\"ja\")') ---")
    ner(text, blank_nlp)

    print()
    print("--- trained nlp ---")
    ner(text, trained_nlp)
