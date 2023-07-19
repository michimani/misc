from datetime import datetime as dt
from json import load as json_load
from os import path
from random import shuffle
from traceback import format_exc
from typing import Final, Optional, Tuple

from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from spacy.cli.train import train as spacy_train
from spacy.language import Language
from spacy.tokens import DocBin, Span


@dataclass
class TrainDataEntity:
    start: int
    end: int
    label: str


@dataclass
class TrainDataRule:
    entities: list[TrainDataEntity]


class TrainData(BaseModel):
    text: str
    rule: TrainDataRule


RAW_DATA_DIR: Final[str] = path.join("data", "train", "raw")
SPACY_DATA_DIR: Final[str] = path.join("data", "train", "spacy")
TRAINED_MODEL_DIR: Final[str] = path.join("data", "train", "trained")


def create_train_data(
    key: str, base_nlp: Language, train_raw_data_path: str
) -> Optional[Tuple[str, str]]:
    train_data_path = path.join(SPACY_DATA_DIR, f"train_data_{key}.spacy")
    dev_data_path = path.join(SPACY_DATA_DIR, f"dev_data_{key}.spacy")

    train_data: list[TrainData] = []
    dev_data: list[TrainData] = []
    with open(train_raw_data_path, "r") as f:
        data = json_load(f)
        shuffle(data)
        for d in data[: len(data) // 2]:
            train_data.append(TrainData(**d))
        for d in data[len(data) // 2 :]:
            dev_data.append(TrainData(**d))

    try:
        start = dt.now()

        def create_spacy_file(
            nlp: Language, db: DocBin, data: list[TrainData], file_path: str
        ):
            for td in data:
                doc = nlp(td.text)
                ents: list[Span] = []
                for entity in td.rule.entities:
                    span = doc.char_span(
                        start_idx=entity.start,
                        end_idx=entity.end,
                        label=entity.label,
                        alignment_mode="expand",
                    )
                    ents.append(span)

                doc.set_ents(ents)
                db.add(doc=doc)

            db.to_disk(file_path)

        # create train data
        train_db = DocBin()
        create_spacy_file(base_nlp, train_db, train_data, train_data_path)

        # create dev data
        dev_db = DocBin()
        create_spacy_file(base_nlp, dev_db, dev_data, dev_data_path)

        diff = dt.now() - start
        print(f"Create train data time: {diff.microseconds/1000} ms")
    except Exception as e:
        print(e)
        print(format_exc())
        return None

    return (train_data_path, dev_data_path)


def train(
    base_nlp: Language,
    train_raw_data_path: str,
    config_path: str = "./train_config.cfg",
) -> Optional[str]:
    event_key = str(dt.timestamp(dt.now()))
    paths = create_train_data(event_key, base_nlp, train_raw_data_path)

    if paths is None:
        return None

    train_data_path, dev_data_path = paths

    output_path = path.join(TRAINED_MODEL_DIR, f"trained_{event_key}")

    start = dt.now()

    try:
        spacy_train(
            config_path=config_path,
            output_path=output_path,
            overrides={
                "paths.train": train_data_path,
                "paths.dev": dev_data_path,
            },
        )
        diff = dt.now() - start
        print(f"Train time: {diff.microseconds/1000} ms ({diff.seconds} s)")
    except Exception as e:
        print(e)
        print(format_exc())
        return None

    return output_path
