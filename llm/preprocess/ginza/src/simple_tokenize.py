import sys

from spacy import load as spacy_load

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python src/simple_tokenize.py <text>")
        sys.exit(1)

    nlp = spacy_load("ja_ginza")

    doc = nlp(args[1])
    for token in doc:
        print(token)
