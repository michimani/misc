import json
import sys

from transformers import pipeline

nlp = pipeline("sentiment-analysis")

if __name__ == "__main__":
    while True:
        try:
            text = input("Enter a sentence: ")
        except KeyboardInterrupt:
            print("\nBye!")
            sys.exit(0)

        if len(text) == 0:
            continue

        result = nlp(text)
        print(json.dumps(result, indent=4))
        sys.exit(0)
