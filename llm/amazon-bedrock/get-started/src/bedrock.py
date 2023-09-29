import json
from typing import Final

import boto3
from mypy_boto3_bedrock import BedrockClient
from mypy_boto3_bedrock.type_defs import FoundationModelSummaryTypeDef
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient


def get_bedrock_client() -> BedrockClient:
    return boto3.client(
        service_name="bedrock",
        region_name="us-east-1",
    )


def get_bedrock_runtime_client() -> BedrockRuntimeClient:
    return boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",
    )


def list_models(client: BedrockClient) -> list[FoundationModelSummaryTypeDef]:
    res = client.list_foundation_models()
    return res["modelSummaries"]


EMBEDDING_MODEL_AMAZON_TITAN: Final[str] = "amazon.titan-embed-text-v1"
CONTENT_TYPE_JSON: Final[str] = "application/json"


def create_embedding(client: BedrockRuntimeClient, input_text: str) -> list[float]:
    res = client.invoke_model(
        body=json.dumps({"inputText": input_text}),
        modelId=EMBEDDING_MODEL_AMAZON_TITAN,
        accept=CONTENT_TYPE_JSON,
        contentType=CONTENT_TYPE_JSON,
    )

    body = json.loads(res["body"].read())
    return body["embedding"]
