from enum import StrEnum

from spacy import load as spacy_load
from spacy.language import Doc, Language

from ginza import set_split_mode

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
