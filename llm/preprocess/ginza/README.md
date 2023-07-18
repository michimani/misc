ginza
===

Get started to using spaCy with Japanese NLP Library GiNZA.

- [spaCy · Industrial-strength Natural Language Processing in Python](https://spacy.io/)
- [GiNZA - Japanese NLP Library | Universal Dependenciesに基づくオープンソース日本語NLPライブラリ](https://megagonlabs.github.io/ginza/)

## Installation

```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install pip --upgrade \
&& pip install -r requirements.lock
```

## Usage

### Simple tokenize.

```bash
ginza ❯ python src/simple_tokenize.py "私はソフトウェアエンジニアです"

私
は
ソフトウェア
エンジニア
です
```

### Split text with some rules.

```bash
ginza ❯ python src/split_text.py '10と24の最大公約数は2です。' 
 
---- SplitType: A ----
10
と
24
の
最大
公約
数
は
2
です
。

---- SplitType: B ----
10
と
24
の
最大
公約数
は
2
です
。

---- SplitType: C ----
10
と
24
の
最大公約数
は
2
です
。
```