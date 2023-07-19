import sys

from utils.nlp import simple_tokenize, split_to_bunsetu

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python src/split_to_sentences.py <text>")
        sys.exit(1)

    doc = simple_tokenize(args[1])
    for span in doc.sents:
        print(span)
        for bspan in split_to_bunsetu(span):
            print(f"\t'{bspan}' ")
            print("\t\t", end="")
            for token in bspan:
                print(f"'{token}' ", end="")
            print()
