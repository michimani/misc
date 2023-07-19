import sys

# from spacy import blank as spacy_blank
from spacy import load as spacy_load

from utils.train import train

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python src/train_ner.py <path to train data>")
        sys.exit(1)

    train_raw_data_path = args[1]

    nlp = spacy_load("ja_ginza")
    trained_model_path = train(nlp, train_raw_data_path)
    if trained_model_path is None:
        print("Failed to train model")
        sys.exit(1)

    print(f"Trained model is saved to {trained_model_path}")
