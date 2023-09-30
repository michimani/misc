import numpy as np
import openai
from openai import Embedding

from embedding import EmbeddingClient

EMBEDDING_MODEL = "text-embedding-ada-002"


class OpenAIEmbeddingClient(EmbeddingClient):
    client: Embedding

    def __init__(self) -> None:
        self.client = openai.Embedding()

    def create_embedding(self, text: str) -> np.ndarray:
        res = self.client.create(input=[text], model=EMBEDDING_MODEL)
        return np.array(res["data"][0]["embedding"])
