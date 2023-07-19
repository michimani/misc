import sys

from utils.nlp import render_dependencies, simple_tokenize

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python src/show_token_dependencies.py <text>")
        sys.exit(1)

    doc = simple_tokenize(args[1])

    render_dependencies(doc)
