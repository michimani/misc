from enum import StrEnum
from typing import Iterable

from spacy import load as spacy_load
from spacy.language import Doc, Language
from spacy.tokens import Span

from ginza import bunsetu_spans, set_split_mode

nlp: Language = spacy_load("ja_ginza")


class SplitMode(StrEnum):
    SplitModeA = "A"
    SplitModeB = "B"
    SplitModeC = "C"


def __tokenize(nlp: Language, text: str) -> Doc:
    return nlp(text)


def simple_tokenize(text: str) -> Doc:
    return __tokenize(nlp, text)


def split_with_mode(text: str, split_mode: SplitMode) -> Doc:
    set_split_mode(nlp, split_mode.value)
    return __tokenize(nlp, text)


def split_to_bunsetu(span: Span) -> Iterable[Span]:
    return bunsetu_spans(span)
