import json
from typing import Final

import boto3
import numpy as np
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient

from embedding import EmbeddingClient

EMBEDDING_MODEL_AMAZON_TITAN: Final[str] = "amazon.titan-embed-text-v1"
CONTENT_TYPE_JSON: Final[str] = "application/json"


class BedrockEmbeddingClient(EmbeddingClient):
    runtime: BedrockRuntimeClient

    def __init__(self) -> None:
        self.runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1",
        )

    def create_embedding(self, text: str) -> np.ndarray:
        res = self.runtime.invoke_model(
            body=json.dumps({"inputText": text}),
            modelId=EMBEDDING_MODEL_AMAZON_TITAN,
            accept=CONTENT_TYPE_JSON,
            contentType=CONTENT_TYPE_JSON,
        )

        body = json.loads(res["body"].read())
        return np.array(body["embedding"])
