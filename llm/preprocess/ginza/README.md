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
text    tag           pos
------  ------------  -----
10      名詞-数詞         NUM
と       助詞-格助詞        ADP
24      名詞-数詞         NUM
の       助詞-格助詞        ADP
最大      名詞-普通名詞-一般    NOUN
公約      名詞-普通名詞-サ変可能  NOUN
数       名詞-普通名詞-一般    NOUN
は       助詞-係助詞        ADP
2       名詞-数詞         NUM
です      助動詞           AUX
。       補助記号-句点       PUNCT

---- SplitType: B ----
text    tag         pos
------  ----------  -----
10      名詞-数詞       NUM
と       助詞-格助詞      ADP
24      名詞-数詞       NUM
の       助詞-格助詞      ADP
最大      名詞-普通名詞-一般  NOUN
公約数     名詞-普通名詞-一般  NOUN
は       助詞-係助詞      ADP
2       名詞-数詞       NUM
です      助動詞         AUX
。       補助記号-句点     PUNCT

---- SplitType: C ----
text    tag         pos
------  ----------  -----
10      名詞-数詞       NUM
と       助詞-格助詞      ADP
24      名詞-数詞       NUM
の       助詞-格助詞      ADP
最大公約数   名詞-普通名詞-一般  NOUN
は       助詞-係助詞      ADP
2       名詞-数詞       NUM
です      助動詞         AUX
。       補助記号-句点     PUNCT
```