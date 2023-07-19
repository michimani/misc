import sys

from utils.nlp import simple_tokenize

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python src/simple_tokenize.py <text>")
        sys.exit(1)

    doc = simple_tokenize(args[1])
    for token in doc:
        print(token)
