import sys

from utils.nlp import render_entities, simple_tokenize

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python src/show_token_dependencies.py <text>")
        sys.exit(1)

    doc = simple_tokenize(args[1])
    print("text\tlabel\tstart\tend")
    for entity in doc.ents:
        print(f"{entity.text}\t{entity.label_}\t{entity.start_char}\t{entity.end_char}")

    render_entities(doc)
