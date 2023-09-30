from abc import ABC, abstractmethod

import numpy as np


class EmbeddingClient(ABC):
    @abstractmethod
    def create_embedding(self, text: str) -> np.ndarray:
        pass


def create_embedding(client: EmbeddingClient, text: str) -> np.ndarray:
    return client.create_embedding(text)


def debug_embedding(embedding: np.ndarray) -> None:
    print(f"Dimensions: {len(embedding)}")
    print(
        f"Embedding: [{embedding[0]}, {embedding[1]} ... {embedding[-2]}, {embedding[-1]}]"
    )
