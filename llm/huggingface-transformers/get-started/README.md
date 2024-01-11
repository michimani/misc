🤗 Transformers
===

[Hugging Face – The AI community building the future.](https://huggingface.co/)

## Installation

### Install MeCab

```bash
brew install mecab
brew install mecab-ipadic
```

### Install Python packages

```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install --upgrade pip \
&& pip install -r requirements.lock
```

## Usage

### Sentiment Analysis

```bash
python src/sentiment_analysis.py

Enter a sentence: This movie is too bolling.

[
    {
        "label": "NEGATIVE",
        "score": 0.9992259740829468
    }
]
```

